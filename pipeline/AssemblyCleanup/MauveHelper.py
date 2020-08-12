from subprocess import call, TimeoutExpired
import os
import utilities
from shutil import copyfile, which, rmtree
import NGS_data_utilities
import pandas as pd
import sys
import seq_utilities
import io
# import shlex

SCRIPT_VERSION = 1 #Aug 2015
SCRIPT_SUBVERSION = 1 #Separaate class from script a little

script_base = os.path.basename(__file__)
_outputBase = '{}_v{}.{}'.format(os.path.splitext(script_base)[0],SCRIPT_VERSION,SCRIPT_SUBVERSION)


mauve_jar = 'Mauve.jar'
Contig_reorder = mauve_jar + ' org.gel.mauve.contigs.ContigOrderer'
Mauve_paths = ['/apps/x86_64/mauve/2.4.0/install/',
               '/home/adam/Software/ThirdParty/mauve_snapshot_2015-02-13/']  
    
    
# Alignment_name =  ##Assign name
# Mauve_path = r'/home/adam/Software/ThirdParty/mauve_snapshot_2015-02-13/linux-x64/progressiveMauve'
# mauve_command  = [Mauve_path]
# mauve_command.append('--hmm-identity=0.95')
# mauve_command.append('--output={}'.format(Alignment_name)) #need filename
# mauve_command += assList
# p_mauve = subprocess.Popen(mauve_command,stdout=open(Alignment_name+'_mauve.stdout','w'),stderr=open(Alignment_name+'_mauve.stderr','w'))

    
def make_output_folder(ref_file, draft_file, outRootDir):
    utilities.safeMakeDir(outRootDir)
    d_base = os.path.splitext(os.path.basename(draft_file))[0]
    r_base = os.path.splitext(os.path.basename(ref_file))[0]
    reorder_output = os.path.join(outRootDir,'{}_ordered_{}'.format(d_base,r_base))
    ##start fresh always 
    if os.path.exists(reorder_output):
        print("Deleting prior working folder...")
        rmtree(reorder_output)
    os.mkdir(reorder_output) 
    return reorder_output

def find_result_file(outDir, draft_file):
    aln_files = [os.path.join(outDir,x) for x in os.listdir(outDir) if x.startswith('alignment')]
    max = len(aln_files)
    aln_folders = [x for x in aln_files if os.path.isdir(x)]
    folder_max = len(aln_folders)
    result_folder = os.path.join(outDir,'alignment{}'.format(folder_max))
    return os.path.join(result_folder,os.path.basename(draft_file))
    
        
#Returns none when everything is ok. Otherwise returns error message.
# def test_executables():
#     result = None
#     if which('progressiveMauve') is None:
#         result = False
#         result = "Cannot call progressiveMauve. Confirm that Mauve is on the path."
#     return result

def get_mauve_dir(full_search, _verbose = False):
    pM_path = which('progressiveMauve')
    if pM_path is None and _verbose:
        print("Executable for ProgressiveMauve is not on the PATH.")
    mauve_dir = None
    if pM_path is not None:
        mauve_dir = os.path.dirname(pM_path) 
    elif full_search:
        for p in Mauve_paths:
            if os.path.isdir(p):
                mauve_dir = p
                if _verbose:
                    print("Found alternative path for Mauve at:"+p)
                break   
    return mauve_dir

def summarize_contig_file(reordered_contigs,draft_file=None):
    stream_list = [io.StringIO()]
    f = open(reordered_contigs,'rt')
    for l in f.readlines():
        sl = stream_list[-1]
        if l == '\n':
            if sl.tell() > 0: ##Create new stream
                stream_list.append(io.StringIO())           
        else:
            sl.write(l)
    i = 0
    contig_stats = {}
    print(len(stream_list))
    for s in stream_list:
        if s.tell() > 0:
            i += 1
            s.seek(0)
            info = s.readline() ##Don't know how to tell if anything remains... seek end, then tell and return to start?
            rc_df = pd.read_table(s)
            rc_df['Length'] = rc_df.right_end - rc_df.left_end + 1
            total_length = sum(rc_df['Length'])
            contig_stats['AlignedLength_{}'.format(i)] = total_length
            contig_stats['AlignedContigs_{}'.format(i)] =  len(rc_df)
            contig_stats['AlignmentClass_{}'.format(i)] = info.strip()
    if draft_file is not None:
        try:
            seq_dict = seq_utilities.seqs_guess_and_parse2dict(draft_file)
            contig_stats['RawContigs'] = len(seq_dict)
            l = 0
            for s in seq_dict.values():
                l += len(s)
            contig_stats['RawLength'] = l
        except IOError:
            pass
    return contig_stats

class MauveHelper():
    
    def __init__(self,find_mauve):
        self.mauve_dir = get_mauve_dir(find_mauve, True)
    
    ############reorder_contigs ####################
    ##This will raise an exception if the output directory already exists. So will Mauve (at least if there is an alignment subfolder)
    def get_command_for_CR(self,ref_file, draft_file, outDir):
        a = 'java -Xmx500m -cp '
        return a + self.mauve_dir + Contig_reorder + ' -output {} -ref {} -draft {}'.format(os.path.abspath(outDir),os.path.abspath(ref_file),os.path.abspath(draft_file))           
    
    def call_contig_mover(self,ref_file, draft_file, outDir):
        cr_command = self.get_command_for_CR(ref_file, draft_file, outDir)
        progFile = os.path.abspath(os.path.join(outDir,'MauveCM_progress.txt'))
        progOut = open(progFile,'wt')
        cwd = os.getcwd()
        os.chdir(self.mauve_dir)
        try:
            if call(cr_command.split(),stdout=progOut,timeout=3600) != 0:
                progOut.close()
                print("Failure to call contig re-order. Command was \n {}".format(cr_command))
                return 1         
            else:
                progOut.close()
                if os.path.isfile(progFile):
                    os.remove(progFile)
        except TimeoutExpired as e:
            print("Timeout (1hr) during contig re-order. Command was \n {}".format(cr_command))
            print(e)
            return 1
        os.chdir(cwd)
        return 0
           
    ##Reorders draft_file according to ref_file, using OutRootDir to write the files. If not result/out location is specified
    ## it            
    def reorder_contigs(self,ref_file, draft_file, outRootDir,resultDir=None,outFile=None):
#         assert (resultDir is not None) or (outFile is not None)
        reorder_stats = None
        outDir = make_output_folder(ref_file, draft_file, outRootDir)
        print("Calling contig mover...")
        if self.call_contig_mover(ref_file, draft_file, outDir) == 0:
            print("Recovering reordered contigs...")
            reordered_draft = find_result_file(outDir,draft_file)
            if os.path.isfile(reordered_draft):
                if isinstance(outFile,str):
                    dest = outFile 
                    copyfile(reordered_draft,dest)
                elif isinstance(resultDir,str) and os.path.isdir(resultDir):
                    dest = utilities.appendToFilename(os.path.join(resultDir,os.path.basename(draft_file)), 'RO')
                    copyfile(reordered_draft,dest)
                else:
                    dest = reordered_draft
                reordered_contigs = os.path.splitext(reordered_draft)[0] + '_contigs.tab'
                reordered_annotation = os.path.splitext(reordered_draft)[0] + '_features.tab'
                reorder_stats = {
                    'DraftFile':draft_file,
                    'ReorderedDraft':dest,
                    'Contig_Report':reordered_contigs,
                    'Reordered_annotation':reordered_annotation                
                                 }        
                if reordered_contigs is not None:
                    reorder_stats.update(summarize_contig_file(reordered_contigs,draft_file))
            else:
                print("Failed to reorder contings for draft file: "+draft_file)
                print("\t The expected result file does not exist: "+reordered_draft)       
                reorder_stats = {
                    'DraftFile':draft_file,
                    'ReorderedDraft':'failure',               
                                 }   
        return reorder_stats
    ##############
               
    
import argparse
def main():
    parser = argparse.ArgumentParser(description='A program to perform batched Mauve contig reordering (and someday more)')
    ### general info
    parser.add_argument('--version','-V',action='version',version='%(prog)s {}.{}'.format(SCRIPT_VERSION,SCRIPT_SUBVERSION))
#     parser.add_argument('-p','--projectID',help='Provide an identifier that will be added to output directory and data table')
#     parser.add_argument('-s','--setting_dir',help='Location of setting files')
#     parser.add_argument('-m','--min_cov',help='Alternate minimum coverage',default=0.8,type=float)

#     parser.add_argument('--debug',action='store_true',help="Preserve intermediate files and do not update reference files")

    ### controls
    parser.add_argument('--find_mauve',action='store_true',help="Search for known Mauve directories if it is not on the path")
    parser.add_argument('--search_subdirectories',action='store_true',help="Search for draft genome files in subdirectories of specified folder")
    parser.add_argument('-wd','--working_directory',help='Working directory for Mauve to align assemblies. Will make a new subdirectory if not specified, starting with: '+_outputBase)
    parser.add_argument('-rd','--result_directory',help='Result directory for reoriented assemblies. Will use top level of working directory if not specified.')
    
    ### required
    parser.add_argument('draft_dir',help='Location of draft assemblies')
    parser.add_argument('reference_genome',help='Reference genome file to orient towards')
    
    
    args = parser.parse_args()
    
    assert os.path.isdir(args.draft_dir), "Draft_dir is not a directory"
    assert os.path.isfile(args.reference_genome), "Reference genome file does not exist"
    working_dir = os.path.abspath(args.working_directory) if args.working_directory else utilities.safeMakeOutputFolder(_outputBase)
    result_dir = os.path.abspath(args.result_directory) if args.result_directory else working_dir
    
    mh = MauveHelper(args.find_mauve)
    if (mh.mauve_dir is None):
        sys.exit("Cannot Find the Mauve path")
    elif not os.path.isfile(mh.mauve_dir + mauve_jar):
        sys.exit("Cannot Find the Mauve jar file. Searched on this path: "+mh.mauve_dir)
    else:
        reorder_stats = []
        draft_genomes = NGS_data_utilities.listGenomeFilesWithNames(os.path.abspath(args.draft_dir), None, args.search_subdirectories, True)
        if len(draft_genomes) > 0:
            for draft_file in draft_genomes['Filename']:
                print('starting with {}'.format(draft_file))
                reorder_stats.append(mh.reorder_contigs(os.path.abspath(args.reference_genome), draft_file, working_dir, result_dir))
        else:
            print("Found no genomes. Exiting")
    try:
        statTable = pd.DataFrame(reorder_stats)
        statTable.to_csv(os.path.join(result_dir,"reorderStats.tab",sep='\t',index=False))
    except Exception as e:
        print("Failure to save statistics...")
        print(e)
#         reorder_stats


# from sys import argv
if __name__ == "__main__":
    if not utilities.has_preferred_python():
        raise Exception("Upgrade your python version")
    main()

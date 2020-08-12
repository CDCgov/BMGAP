#! /bin/env python3

### 
##by Adam Retchless
## July 16, 2015, script_version 0.3
### Expects python 3.4. Requires Pandas. Matplotlib is optional.

SCRIPT_VERSION = 1.1 #adding skesa format
SCRIPT_SUBVERSION =  1
import re
import pandas as pd
has_plt = False
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    has_plt = True
except ImportError:
    print("Cannot produce plots without the pyhon module 'matplotlib'")

# from Bio import SeqIO
import os
import time
# from shutil import copyfile
from collections import defaultdict, Counter
# import itertools
# import functools
# import urllib.request 
import utilities
import seq_utilities
# import shlex
###This could be pulled from seq_utils...
from Bio.Alphabet import IUPAC
unambig = IUPAC.IUPACUnambiguousDNA.letters
unambig_set = set(unambig)
ambig_all_set = set(IUPAC.IUPACAmbiguousDNA.letters)
ambig_only_set = ambig_all_set.difference(unambig_set)

script_base = os.path.basename(__file__)
_outputBase = '{}_v{}.{}'.format(os.path.splitext(script_base)[0],SCRIPT_VERSION,SCRIPT_SUBVERSION)


my_file = __file__
if os.path.islink(my_file):
    my_file = os.path.realpath(my_file)
SCRIPT_DIR, SCRIPT_NAME = os.path.split(my_file)
SCRIPT_DIR = os.path.abspath(SCRIPT_DIR)

qual_targets = [20,30,40,50] #Cutoff qualities for reporting low-quality bases; needs to be increasing, because we want values lower than (or equal to) target
quality_head = "Bases_Under_Q"
feature_head = 'Feature_Count'

spades_description_re = re.compile(r'((.+)_ctg_\d+ )?NODE_\d+_length_(\d+)_cov_(\d+(\.\d+)?)(_ID_\d+)?') #note: preceeded by assembly name
skesa_description_re = re.compile(r'(Contig_\d+)_(\d+(\.\d+)?)')
ContigHeaders = ['Contig_Name','Contig_Size','Coverage','Contig'] 
def parse_SPADES(contigs,oldVersion=False,export_contig_data=None,export_contig_graph=None):
    result = []
    for c in contigs: 
        spades_stats = parse_SPADES_contig(c,oldVersion=oldVersion)
        if spades_stats is not None:
            result.append(spades_stats)
        else:
            print("Failure to parse SPADEs contig")
    contig_table = pd.DataFrame(result)  
    ### TODO: remove this to a higher level          
    if has_plt:
        try:
            if isinstance(export_contig_graph,str):
                fig = contig_table.plot(kind='scatter', x='Contig_Size',y='Coverage',logx=True,logy=True)
                fig = fig.get_figure()
                fig.savefig(export_contig_graph)   
        except Exception as e:
            print('Failed to save contig stats scatterplot at '+export_contig_graph)
            utilities.printExceptionDetails(e)
    try:
        if isinstance(export_contig_data,str):
            contig_table[ContigHeaders[0:-1]].to_csv(export_contig_data,index=False)
    except:
        print('Failed to save contig stats table at '+export_contig_data)
        raise
    return contig_table

def parse_SPADES_contig(c,oldVersion=False): 
    seq_match = spades_description_re.match(c.description)
    if not seq_match:
#         print("Improper formatting for {}".format(c.description))
        raise ValueError ("Improper formatting for spades {}".format(c.description))
    if seq_match:
        length_text = seq_match.groups()[2]
        try:
            contig_length = int(length_text)
        except:
            print("Failure to parse contig length: "+length_text)
            contig_length = len(c)
            raise
#         else:
#             if not oldVersion: ##bug in 3.1; fixed by 3.5
#                 assert contig_length == len(c), "Documented length of {} for contig {} does not match observed length {}".format(contig_length, c.name,len(c))
        coverage_text = seq_match.groups()[3]
        try:
            coverage = float(coverage_text)
        except:
            print("Failure to parse coverage :"+coverage_text)    
            raise
#             else:            
#                 print("Coverage: {}".format(coverage))
        return pd.Series((c.id,contig_length,coverage,c),ContigHeaders)
    else: 
        print("not")
        return None

def parse_SKESA(contigs,export_contig_data=None,export_contig_graph=None):
    result = []
    for c in contigs: 
        skesa_stats = parse_SKESA_contig(c)
        if skesa_stats is not None:
            result.append(skesa_stats)
        else:
            print("Failure to parse skesa contig")
    contig_table = pd.DataFrame(result)  
    ### TODO: remove this to a higher level          
    if has_plt:
        try:
            if isinstance(export_contig_graph,str):
                fig = contig_table.plot(kind='scatter', x='Contig_Size',y='Coverage',logx=True,logy=True)
                fig = fig.get_figure()
                fig.savefig(export_contig_graph)   
        except Exception as e:
            print('Failed to save contig stats scatterplot at '+export_contig_graph)
            utilities.printExceptionDetails(e)
    try:
        if isinstance(export_contig_data,str):
            contig_table[ContigHeaders[0:-1]].to_csv(export_contig_data,index=False)
    except:
        print('Failed to save contig stats table at '+export_contig_data)
        raise
    return contig_table
    
def parse_SKESA_contig(c):
    seq_match = skesa_description_re.match(c.description.strip())
    if not seq_match:
#         print("Improper formatting for {}".format(c.description))
        raise ValueError ("Improper formatting for skesa {}".format(c.description))
    contig_length = len(c)    
    if seq_match:
        coverage_text = seq_match.groups()[1]
        try:
            coverage = float(coverage_text)
        except:
            print("Failure to parse coverage :"+coverage_text)    
            raise
#             else:            
#                 print("Coverage: {}".format(coverage))
        return pd.Series((c.id,contig_length,coverage,c),ContigHeaders)
    else: 
        print("not")
        return None    

#assemble options are spades, skesa
def getContigStats(contig_iterator,hasQual,assembler=None,oldVersion=False):
    if isinstance(assembler,str):
        assembler = assembler.upper()
        print("Assembler is {}".format(assembler))
    else:
        print("No assembler specified")
    contig_records = []
    for contig in contig_iterator:
        ##### Quality scores
        if hasQual:
            qual = contig.letter_annotations["phred_quality"]  
            qual_threshold = bin_quality_scores(qual,qual_targets)
        else:
            qual_threshold = defaultdict(int) #only modified by fastq
        ##Record contig-specific measures,
        if assembler == 'SPADES':
            this_record = parse_SPADES_contig(contig,oldVersion=oldVersion) ##Note, somewhere "Coverage" is being converted to string from float
        elif assembler == 'SKESA':
            this_record = parse_SKESA_contig(contig)
        else:
            this_record = { 'Contig_Name':contig.id,'Contig_Size':str(len(contig))}
        ###Count ambiguous characters
        nuc_counts = Counter(str(contig.seq))
        ambig_upper_lower = set([i.lower() for i in ambig_only_set] + [i.upper() for i in ambig_only_set])
        ambig_counts = 0
        for item in ambig_upper_lower:
            if item in nuc_counts:
                ambig_counts += nuc_counts[item]
        ### Confirm that remainder are unambigous
        unambig_upper_lower =set([i.lower() for i in unambig_set] + [i.upper() for i in unambig_set])
        unambig_counts = 0
        for item in unambig_upper_lower:
            if item in nuc_counts:
                unambig_counts += nuc_counts[item] 
        assert ambig_counts + unambig_counts == len(contig), "Ambiguous characters not properly counted"       
        this_record['Ambiguous_nucleotides'] = ambig_counts
        if len(qual_threshold) > 0: ##TODO: test this with PacBio data
            for i in qual_threshold.keys():
                header = quality_head + "{}".format(i)
                this_record[header] = qual_threshold[i]
        if contig.features is not None:
            this_record[feature_head] = len(contig.features)
        contig_records.append(this_record)
    ##Record whole-genome traits
    return pd.DataFrame(contig_records,dtype=str)

def bin_quality_scores(qual,targets):
    ### count bases at each quality score
    qual_counter = defaultdict(int)              
    for x in qual: qual_counter[x] += 1
    ## count the numeber that fall beflow the threshold
    qual_thresholds = defaultdict(int)
    if len(qual_counter) > 0:
        #count for this contig
        max_score = max(qual_counter.keys())
        qual_bases = 0
        for i in range(0,max_score+1): 
            qual_bases += qual_counter[i]
            if i in targets:
                qual_thresholds[i] += qual_bases
    return qual_thresholds

def calcN50_stats(size_list, thresholds = None):
    if thresholds is None:
        thresholds = [50,75,90]
    assert max(thresholds) < 100, "Cannot calculate N100 or greater"
    assert min(thresholds) > 0, "Cannot calculate N0 or less"
    sortedSizes = sorted(size_list,reverse=True)#descending
    totalSize = sum(sortedSizes)
    threshold_sizes = {x: x*totalSize/100 for x in thresholds}
    cumulative = 0
    result = dict()
    for key in sorted(threshold_sizes.keys()): #ascending
        size = threshold_sizes[key] #target
        while cumulative < size: #Since size > 0, will always enter loop on first run
            x = sortedSizes.pop(0) ##This should never reach the end
            cumulative += x
        result[key] = x ##This will carry over from previous round if cumulative is already >= size
    return result

#filelist or frame must be either a list of filepaths, or a frame with a "Filename" field
def calculateStats(filelist_or_frame,out_file=None,ass_format=None,image_dir=None,save_details=False):
    if isinstance(filelist_or_frame,list):
        filelist = filelist_or_frame
        fileframe = None
    elif isinstance(filelist_or_frame,pd.DataFrame):
        filelist = filelist_or_frame.Filename
        fileframe = filelist_or_frame
    else:
        raise ValueError("can only calculate stats on a list of filenames or a DataFrame with a Filename field")
    if len(filelist) == 0:
        raise ValueError("AssemblyStats CalculateStats requires a list of files with length > 0. Contact developer")
    assFrame = None
    if isinstance(image_dir,str):
        utilities.safeMakeDir(image_dir)    
    if len(filelist) > 0:
        assemblyList = []
        for filename in filelist:
            if isinstance(ass_format,str):
                assembler = ass_format
            elif ('spades' in filename):
                assembler = 'spades'
                print("Guessing assembler as {}".format(assembler))
            elif ('skesa' in filename):
                assembler = 'skesa'
                print("Guessing assembler as {}".format(assembler))
            else:
                assembler = None
            genome_format,_ = utilities.guessFileFormat(filename)
            AssInfo = {'Filename':filename} ##This will report data for all files provided. Junk files will have 0 contigs and 0 size
            if genome_format is None:
                AssInfo['Note']='Could not identify genome format'  
            else:
                try:
                    contig_list = seq_utilities.seqs_guess_and_parse2list(filename)                                       
                    if isinstance(contig_list,list) and len(contig_list) > 0:
                        contigFrame = getContigStats(contig_list,hasQual = (genome_format == 'fastq'),assembler=assembler) 
                        if 'Coverage' in contigFrame.columns:
                            contigFrame['Coverage'] = contigFrame['Coverage'].astype(float) ##Note: Coverage is being cast to float in getSpadesStats, but somehow becomes string in this frame.
                        if 'Contig_Size' in contigFrame.columns:
                            contigFrame['Contig_Size'] = contigFrame['Contig_Size'].astype(int)
                        if save_details:
                            contig_file = utilities.setExt(utilities.appendToFilename(filename,'_contigs'),'.xlsx')
                            contigFrame.to_excel(contig_file)
                        assert len(contig_list) == len(contigFrame), "Not all contigs are in dataframe"  
                        if isinstance(image_dir,str) and os.path.isdir(image_dir):
                            if has_plt:
                                if ('Coverage' in contigFrame.columns) and ('Contig_Size' in contigFrame.columns):
                                    tempFrame = contigFrame[['Coverage','Contig_Size']].copy()
                                    try:
                                        raw_filename = os.path.join(image_dir,os.path.basename(filename))
                                        image_file = utilities.setExt(raw_filename, 'png') ##Note: only reason to do                                     
                                        if isinstance(image_file,str):
                                            fig = tempFrame.plot(kind='scatter', x='Contig_Size',y='Coverage',logx=True,logy=True)
                                            fig = fig.get_figure()
                                            fig.savefig(image_file)    
                                    except Exception as e:
                                        print('Failed to save contig stats scatterplot at '+image_file)
                                        for c in tempFrame.columns:
                                            print(tempFrame[c])
                                        utilities.printExceptionDetails(e)
                                    else:
                                        try:
                                            plt.close(fig)
                                        except:
                                            print("Failed to close image...")  
                                elif assembler in ['skesa','spades']:
                                    print("Unable to produce contig stats scatterplot because necessary fields are not present ('Contig_Size' and 'Coverage')")                     
                        AssInfo['Contig_Count']=str(len(contig_list))
                        contigSizes = contigFrame['Contig_Size'].astype(int)
                        assemblySize = sum(contigSizes)                
                        AssInfo['Bases_In_Contigs'] = str(assemblySize)                   
                        largeContigs = contigSizes > 10000
                        AssInfo['Large_Contig_Count'] = str(sum(largeContigs))
                        AssInfo['Small_Contig_Count'] = str(sum(~largeContigs))
                        AssInfo['Bases_In_Large_Contigs'] = str(sum(contigSizes[largeContigs]))
                        AssInfo['Bases_In_Small_Contigs'] = str(sum(contigSizes[~largeContigs]))
                        emptyContigs = contigSizes == 0
                        if sum(emptyContigs) > 0:
                            print('\n#### WARNING #### EMPTY CONTIGS ########\n')                           
                            print('\n\t'.join(contigFrame[emptyContigs].Contig_Name.tolist()))
                            print('\n########################################\n')
                        if 'Coverage' in contigFrame.columns:
                            contigCoverage = contigFrame['Coverage'] ##should be float, but seems to get converted to a string with some versions
                            if len(contigCoverage[largeContigs]) > 0:
                                min_c = min(contigCoverage[largeContigs])
                                AssInfo['Min_Coverage_Large_Contigs'] = str(min_c) 
                                max_c = max(contigCoverage[largeContigs])
                                AssInfo['Max_Ratio_of_Coverage_Large_Contigs'] = '{:0.2f}'.format(max_c/min_c) 
                                lowC_contigs = contigFrame['Coverage'] < (min_c / 2)
                                AssInfo['Low_Coverage_Contig_Count'] = sum(lowC_contigs)
                                AssInfo['Low_Coverage_Contig_Bases'] = sum(contigFrame.loc[lowC_contigs,'Contig_Size'])
                            else:
                                AssInfo['Min_Coverage_Large_Contigs'] =  'N/A'
                                AssInfo['Max_Ratio_of_Coverage_Large_Contigs'] = 'N/A' 
                                AssInfo['Low_Coverage_Contig_Count'] = 'N/A'
                                AssInfo['Low_Coverage_Contig_Bases'] = 'N/A'                      
                            coverageProduct = contigFrame['Contig_Size'].astype(int) * contigFrame['Coverage']   
                            coverageProductSum = sum(coverageProduct)    
                            meanCoverage = coverageProductSum/assemblySize
                            AssInfo['Mean_Coverage'] = meanCoverage            
                            lowC_contigs = contigFrame['Coverage'] < (meanCoverage / 2)
                            AssInfo['HalfCov_Contig_Count'] = sum(lowC_contigs)
                            AssInfo['HalfCov_Contig_Bases'] = sum(contigFrame.loc[lowC_contigs,'Contig_Size'])
                        if feature_head in contigFrame:
                            featureCounts = contigFrame[feature_head].astype(int)
                            AssInfo[feature_head] = sum(featureCounts)
                        ### Sum ambiguous nucleotides
                        ambigCounts = contigFrame['Ambiguous_nucleotides'].astype(int)
                        AssInfo['Ambiguous_nucleotides']=sum(ambigCounts)
                        ## Import the quality scores
                        for c in contigFrame.columns:
                            if c.startswith(quality_head):
                                AssInfo[c] = str(sum(contigFrame[c]))            
                        ##Calculate N50 and N90
                        N_stats = calcN50_stats(contigSizes.tolist(),thresholds=[50,75,90])
                        for n,size in N_stats.items():
                            header = "N{}".format(n)
                            AssInfo[header] = str(size)
#                         assemblyList.append(AssInfo)
                    else:
                        print("failed to parse file: "+filename)
                        AssInfo['Note'] = 'No sequences parsed from file'
                except Exception as e:
                    print("Warning: failed to assess file: " + filename)
                    print("Exception: {}".format(e))
                    raise
             
            if 'Bases_In_Contigs' not in AssInfo:
                AssInfo['Bases_In_Contigs'] = 0 
            if 'Contig_Count' not in AssInfo:
                AssInfo['ContigCount'] = 0
            assemblyList.append(AssInfo)
        if len(assemblyList) > 0:
            print("Stats for {} assemblies.".format(len(assemblyList)))
            assFrame = pd.DataFrame(assemblyList)
            if isinstance(fileframe,pd.DataFrame):
                saveFrame = pd.merge(fileframe,assFrame,on='Filename')
            else:
                saveFrame = assFrame.set_index('Filename')
            if (out_file is not None):
                try:
                    saveFrame.to_csv(out_file)
                except Exception as e:
                    print(saveFrame.to_csv())
                    print()
                    print("Failed to print to target file {}. \nPrinted results to screen (above)".format(out_file))
                    utilities.printExceptionDetails(e)
        else:
            print("Failed to evaluate assemblies...")
            print("attempted to evaluate the following files:"+"\n".join(filelist))
    return assFrame

def BeforeAndAfter(pre_stats,post_stats):
    rename_raw = {x:x+'_raw' for x in pre_stats.columns}       
    merged_stats= pd.merge(pre_stats.rename(columns=rename_raw),post_stats,left_index=True,right_index=True,how='outer')#Each should have a single index.
    merged_stats.fillna('N/A', inplace=True)
    try:
        if ('Bases_In_Contigs' in merged_stats) and ('Bases_In_Contigs_raw' in merged_stats): ##Should always be integers
            merged_stats['Discarded_Bases'] = merged_stats.Bases_In_Contigs_raw.astype(int) - merged_stats.Bases_In_Contigs.astype(int)
            merged_stats['Discarded_Percent'] = 100*merged_stats.Discarded_Bases.astype(int)/merged_stats.Bases_In_Contigs_raw.astype(int)
            if ('HalfCov_Contig_Bases' in merged_stats):
                merged_stats['HalfCov_Percent'] = 100*merged_stats.HalfCov_Contig_Bases/merged_stats.Bases_In_Contigs.astype(int)
    except Exception as e:
        utilities.printExceptionDetails(e)
    return merged_stats    

import argparse        
def main():
    print("")
    print("Running {} from {} at {}".format(_outputBase,os.getcwd(),time.ctime())) #SCRIPT_NAME
    print("...script is found in {}\n".format(SCRIPT_DIR)) 
    
    parser = argparse.ArgumentParser(description='A program to provide summary statistics for an assembly.')    
    parser.add_argument('directory',help='folder with assembly files to evaluate')
    parser.add_argument('--output','-o',help='File to write summary stats to (default is {}.csv in Assembly Directory'.format(_outputBase))
    parser.add_argument('--spades',action='store_true',help='All contigs are spades, even if filename does not days so. (default is to guess based on "spades" in filename.)')
    parser.add_argument('--extension','-e',help="Limit analysis to files with the given suffix")
    parser.add_argument('--save_contig_details',action='store_true')
    

#     ##Info
#     parser.add_argument('force','-f',help='Force overwrite of output')
    parser.add_argument('--version','-V',action='version',version='%(prog)s {}'.format(SCRIPT_VERSION))
#     parser.add_argument('--circularize_with_Ns',type=int,default=0,help='Assume that contigs are circular and add this many Ns to fill circle. Default is to leave contig broken')
#     parser.add_argument('--reference','-r',help="Reference genome for contig reordering")
#     parser.add_argument('--coverage','-c',help='Minimum coverage to keep contig (extracted from SPADES contig description)',default=10)
#     parser.add_argument('--length','-l',help='Minimum length to keep contig',default=250)
#     parser.add_argument('--assembler','-a',default='Unknown',help="Assembler used to produce contigs (e.g. SPADES). Provides description of read coverage for cleaning")
#     parser.add_argument('--debug',action='store_true',help='Create a temporary repository in current directory')

    args = parser.parse_args()
    input_folder = os.path.abspath(args.directory)
    assert os.path.isdir(input_folder),"Directory is invalid"
    out_file = args.output if args.output else os.path.join(input_folder,_outputBase+".csv")
#     dataFrame = NGS_data_utilities.
    filelist = [os.path.join(input_folder,x) for x in os.listdir(input_folder)]
    filelist = [x for x in filelist if os.path.isfile(x)]
    print('Identified {} files in directory.'.format(len(filelist)))
    if args.extension:
        filelist = [x for x in filelist if x.endswith(args.extension)]
        print('Focusing on {} files with the extension "{}"'.format(len(filelist),args.extension))
    if len(filelist) > 0:
        if args.spades:
            assFormat = 'spades'
        else:
            assFormat = None
        calculateStats(filelist,out_file,assFormat,save_details=args.save_contig_details)
#         assemblyList = []        
#         for filename in filelist:
#             print
#             try:
#                 genome_format,genome_compressed = utilities.guessFileFormat(filename)
#                 is_spades = args.spades or ('spades' in filename)
#                 if genome_format is not None:
#                     AssInfo = {'Filename':filename}
#                     in_file = os.path.join(input_folder,filename)
#                     with utilities.flexible_handle(in_file,genome_compressed,'rt') as fin: 
#                         contig_list = [x for x in SeqIO.parse(fin,genome_format)] 
#                     assert len(contig_list) > 0, "Failed to parse contig file"+ in_file
#                     contigFrame = getContigStats(contig_list,hasQual = (genome_format == 'fastq'),isSPADES=is_spades)      
#                     assert len(contig_list) == len(contigFrame), "Not all contigs are in dataframe"  
#                     AssInfo['Contig_Count']=str(len(contig_list))
#                     contigSizes = contigFrame['Contig_Size'].astype(int)
#                     assemblySize = sum(contigSizes)
#                     AssInfo['Bases_In_Contigs'] = str(assemblySize) 
#                     largeContigs = contigSizes > 10000
#                     AssInfo['Large_Contig_Count'] = str(sum(largeContigs))
#                     AssInfo['Small_Contig_Count'] = str(sum(~largeContigs))
#                     AssInfo['Bases_In_Large_Contigs'] = str(sum(contigSizes[largeContigs]))
#                     AssInfo['Bases_In_Small_Contigs'] = str(sum(contigSizes[~largeContigs]))
#                     if 'Coverage' in contigFrame.columns:
#                         contigCoverage = contigFrame['Coverage'] ##should be float
#                         if len(contigCoverage[largeContigs]) > 0:
#                             min_c = min(contigCoverage[largeContigs])
#                             AssInfo['Min_Coverage_Large_Contigs'] = str(min_c) 
#                             max_c = max(contigCoverage[largeContigs])
#                             AssInfo['Max_Ratio_of_Coverage_Large_Contigs'] = '{:0.2f}'.format(max_c/min_c) 
#                             lowC_contigs = contigFrame['Coverage'] < (min_c / 2)
#                             AssInfo['Low_Coverage_Contig_Count'] = sum(lowC_contigs)
#                             AssInfo['Low_Coverage_Contig_Bases'] = sum(contigFrame.loc[lowC_contigs,'Contig_Size'])
#                         else:
#                             AssInfo['Min_Coverage_Large_Contigs'] =  'N/A'
#                     ### Sum ambiguous nucleotides
#                     ambigCounts = contigFrame['Ambiguous_nucleotides'].astype(int)
#                     AssInfo['Ambiguous_nucleotides']=sum(ambigCounts)
#                     ## Import the quality scores
#                     for c in contigFrame.columns:
#                         if c.startswith(quality_head):
#                             AssInfo[c] = str(sum(contigFrame[c]))            
#                     ##Calculate N50 and N90
#                     N_stats = calcN50_stats(contigSizes.tolist(),thresholds=[50,75,90])
#                     for n,size in N_stats.items():
#                         header = "N{}".format(n)
#                         AssInfo[header] = str(size)
#                     assemblyList.append(AssInfo)
#             except Exception as e:
#                 print("Warning: failed to assess file: " + filename)
#                 print("Exception: {}".format(e))
#         
#         if len(assemblyList) > 0:
#             assFrame = pd.DataFrame(assemblyList)
#             assFrame.set_index('Filename', inplace=True)
#             try:
#                 assFrame.to_csv(out_file)
#             except:
#                 print(assFrame.to_csv())
#                 print()
#                 print("Failed to print to target file {}. \nPrinted results to screen (above)".format(out_file))
#         else:
#             print("Failed to evaluate assemblies...")
#             print("attempted to evaluate the following files:"+"\n".join(filelist))
    else:
        print("Found no files in "+input_folder)

    
    
            
    print("Fields:")
    print("\t Large Contigs are > 10kb")
    print("\t HalfCov is < 1/2 of the assembly-wide mean depth of coverage")
    print("\t Low coverage is < 1/2 of the lowest coverage on a large contig")
    print("\t Max ratio of coverage is the ratio of the max mean coverage for a large contig and the min mean coverage for a large contig.")
    print("BOOYA!")

    
    
    ##Establish shared settings
    
    
    ##Run program
        ##Run the program
#     result = args.func(args)
#     if result != 0:
#         parser.print_usage()
        
    
        
    


if __name__ == "__main__":
    if not utilities.has_preferred_python():
        raise Exception("Upgrade your python version")
    main()     
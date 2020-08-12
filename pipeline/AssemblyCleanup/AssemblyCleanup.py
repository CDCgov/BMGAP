#! /bin/env python3

### 
##by Adam Retchless
## April 24, 2015, script_version 0.3
SCRIPT_VERSION = 1
SCRIPT_SUBVERSION = 23



#pylint: disable=global-statement, broad-except
import re
import pandas as pd
from Bio import SeqIO, SeqRecord
import os
import sys
# import gzip
# import zlib
# import stat
import time
# from shutil import copyfile
# from collections import defaultdict
# import itertools
# import functools
# import urllib.request 
import utilities
import seq_utilities
import BLASThelpers
from BLASThelpers import BLASTheaders as bh
from Bio.Blast.Applications import NcbiblastnCommandline
import shlex
import NGS_data_utilities
import AssemblyStats
from MauveHelper import MauveHelper, mauve_jar

script_base = os.path.basename(__file__)
_outputBase = '{}_v{}.{}'.format(os.path.splitext(script_base)[0],SCRIPT_VERSION,SCRIPT_SUBVERSION)

my_file = __file__
if os.path.islink(my_file):
    my_file = os.path.realpath(my_file)
SCRIPT_DIR, SCRIPT_NAME = os.path.split(my_file)
SCRIPT_DIR = os.path.abspath(SCRIPT_DIR)

ContigHeaders = ['Contig_ID','Length','Coverage','Contig']
RO_argset = set(['circle_new_start','reverse_contig','closed_circle','broken_circle','circularize_with_Ns','reference'])
DIS_argset = set(['length','coverage','assembler','Mean_Coverage'])

# def cleanup_SPADES_folder(input_folder,output_folder, **kwargs):
#     utilities.safeMakeDir(output_folder)
#     for filename in os.listdir(input_folder):
#         if filename.endswith('.fasta'):
#             in_file = os.path.join(input_folder,filename)
#             base = os.path.basename(filename)
#             out_file = os.path.join(output_folder,base)
#             kwargs['export_contig_data'] = out_file+'_ContigStats.csv' ##Override any that was passed, since we have multiple files
#             cleanup_SPADES_file(in_file,out_file,**kwargs)

# def cleanup_SPADES_file(input_file, output_file, **kwargs):
#     with open(input_file,'rt') as fin:
#         seqs = [c for c in SeqIO.parse(fin,'fasta')]
#     cleaned = cleanup_SPADES(seqs,**kwargs)
#     with open(output_file,'wt') as fout:
#         SeqIO.write(cleaned,fout,'fasta')

def cleanup_SPADES(contigs,minimum_length, minimum_coverage, export_contig_data=None,discard_file=None,export_contig_graph=None):
    contig_table = AssemblyStats.parse_SPADES(contigs,export_contig_graph=export_contig_graph,export_contig_data=export_contig_data)
    good_length = contig_table['Contig_Size'] > minimum_length
    if (contig_table.Coverage.isnull().any()):
        raise Exception("Null value in coverage table during Assembly Cleanup. Unable to filter")
        good_contig_bool = good_length
    else:
        good_coverage = contig_table['Coverage'] > minimum_coverage
        good_contig_bool = good_coverage & good_length
    good_contig_table = contig_table[good_contig_bool]
    good_contigs = good_contig_table['Contig'].tolist()
    if discard_file is not None:
        try:
            discard_contigs = contig_table[~good_contig_bool]['Contig'].tolist()
            SeqIO.write(discard_contigs,discard_file,utilities.guessFileFormat(discard_file)[0]) 
        except Exception as e:
            print(e)
            raise
    return good_contigs

## set format for BLAST tabular output
_BLASTheaderList = ['qseqid','sseqid','length','qcovhsp','qstart','qend','qlen','sstart','send','slen','qcovs',
                    'evalue','bitscore','pident','sstrand']
_outfmt_str, _outfmt_head = BLASThelpers.BLASTtableCommandAndHeaders(_BLASTheaderList)

### This reorients closed circular contigs so that they start at the same place as a reference contig
### This was intended for both raw and reference to be single contigs, but it is not necessary (though multi-contig is untested)
## Raw_contig is a list of SeqRecords (should be single)
## Reference file is the sequence file that you want to align to 
def reorientClosedChromosome(raw_contig,reference_file,N_padding=-1,working_dir=None,set_steps=5,set_window=5000):
    temp_dir = None
    if isinstance(working_dir,str):
        try:
            utilities.safeMakeDir(working_dir)
            temp_dir = working_dir
        except IOError:
            pass ##Leave temp_dir as None
    if temp_dir is None:
        temp_dir = utilities.safeMakeOutputFolder('AssemblyCleanup_temp_')
    ## Setup blast database for the sequences you are searching against
    raw_contig_dict = SeqIO.to_dict(raw_contig)
    raw_contig_file = os.path.join(temp_dir,utilities.makeSafeName("-".join(raw_contig_dict.keys())))
    SeqIO.write(raw_contig,raw_contig_file,'fasta')
    db_name = os.path.join(temp_dir,os.path.basename(raw_contig_file))
    BLASThelpers.makeblastdb(raw_contig_file)
    ##Get several chunks near the beginning of the reference file, as query
    ref_seqs = seq_utilities.seqs_guess_and_parse2list(reference_file)
    for rs in ref_seqs:
        rename = re.sub('\W','_',rs.name)
        steps = set_steps
        window = set_window
        expected_search_length = steps * window - 1
        if len(rs) < expected_search_length:
            steps = len(rs) // window
            if steps == 0:
                steps = 1
                window = len(rs)
            search_length = steps * window
            print("Reference sequence is only {}bp; dropping search sequence from {} to {}".format(len(rs),expected_search_length,search_length))
        else:
            search_length = expected_search_length
        SearchWindows = []
        for i in range(0,search_length,window):
            end_base = i + window
            contig = rs[i:end_base] 
            contig.id = 'fragment_{}_to_{}'.format(i,end_base)
            SearchWindows.append(contig)
        query_basename = rename+'_WindowsQuery.fasta'
#         re.sub('[^\w\s-]', '', value).strip().lower())
        query_filename = os.path.join(temp_dir,query_basename)
        with open(query_filename,'wt') as seq_out:
            SeqIO.write(SearchWindows,seq_out,'fasta')
        ##Run BLAST
        outfile = os.path.join(temp_dir,rename + '_' + os.path.basename(db_name))
        ##Note: may need to have "high stringency" and "low stringency" options. This is low stringency (for mapping to distant relatives). High stringency would increase perc_identity here and the qcovs filtering of "results"
        blast_cline = NcbiblastnCommandline(query=shlex.quote(query_filename),db=shlex.quote(db_name),outfmt=_outfmt_str,out=shlex.quote(outfile),evalue=1E-100,perc_identity=80,qcov_hsp_perc=25,num_threads=2)   
        stdout = stderr = None
        try:
            stdout, stderr = blast_cline()
        except Exception as e:
            print("Blast failed on {} with {}...output below...".format(rename,reference_file))
            print("\t{}".format(stdout))
            print("\t{}".format(stderr))
            print(e)
            raise
        results = pd.read_table(outfile,names=_outfmt_head)#No headers in file 
        results = results[results[bh['qcovs']] > 50].sort(bh['bitscore'],ascending=False)  ##Should already be sorted by bitscore
        full_start = full_end = 0 ##BLAST uses a 1 index
        first_hit = None
        coherent_fragments = 0
        for w in SearchWindows:
            window_hits = results[results[bh['qseqid']] == w.id]
            if len(window_hits) > 0:
                hit = window_hits.iloc[0]
                start = hit[bh['sstart']]
                end = hit[bh['send']]
                contig = hit[bh['sseqid']]
                forward = start < end
                if first_hit is None: ##Serves as a sign that there was no prior hit
                    first_hit = hit
                    hit_contig = contig
                    full_start = start
                    full_end = end
                    full_forward = forward
                else: ##Check that it is consistent with prior
                    in_order = (contig == hit_contig) 
                    in_order &= full_forward == forward
                    in_order &= (full_end < start) == full_forward
                    in_order &= abs(end - full_end) < 2 * window
                    if in_order:
                        full_end = end
                        coherent_fragments += 1
                    else:
                        print("Warning: Contig {} is not in order. \nStopping".format(w.id))
                        break #For search windows
            else:
                print("Warning: Failed to find a match to fragment {}".format(w.id))
                if coherent_fragments > 0:
                    print('Stopping since we have an anchor already')
                    break #For search windows
        if coherent_fragments > 0:      
            print("Shifting contig {} ({} bp)".format(hit_contig,len(raw_contig_dict[hit_contig])))      
            new_contigs = shiftCirclarChromosome(raw_contig_dict[hit_contig],full_start,not full_forward,N_padding)
            del raw_contig_dict[hit_contig]
            for new_contig in new_contigs:
                raw_contig_dict[new_contig.id] = new_contig
                assert len(new_contig) != 0, 'Contig with length 0. Aborting. Contact developer'
            print('Rotating contig: {}'.format(hit_contig))
            print('Starting at {}'.format(full_start))
            if full_forward:
                print("keeping orientation")
            else:
                print("Reverse complement")
        else:
            print('Aborting: Failed to identify the start position based on the reference genome.')
            print("\t Reorient contig by specifying args.circle_new_start and/or args.reverse_contig")
            blast_results = outfile+'.tab'
            print('\t Saving BLAST results at '+blast_results)
            results.to_csv(blast_results,sep='\t') 
            return None
    return [x for x in raw_contig_dict.values()]

def reorientContigs(raw_contigs,reference_file,working_dir,name=None,input_format=None):
    utilities.safeMakeDir(working_dir)
    mh = MauveHelper(True) ##looks in pre-defined location (mulitple versions)
    if (mh.mauve_dir is None):
        sys.exit("Cannot Find the Mauve path")
    elif not os.path.isfile(mh.mauve_dir + mauve_jar):
        sys.exit("Cannot Find the Mauve jar file. Searched on this path: "+mh.mauve_dir)
    else:
        if name is None:
            name = 'noName'+time.strftime("%H%M%S")
        temp_ext = 'fasta'
        if input_format is None:
            input_format = 'fasta'
        elif input_format in ['gb','embl']:
            input_format = 'gb'
            temp_ext = 'gbk'
        elif input_format != 'fasta':
            print("Reorient contigs input format not recognized. Using raw FASTA.")
            input_format = 'fasta'
        assembly_file = os.path.join(working_dir,name+'_intermediate.'+temp_ext)
        SeqIO.write(raw_contigs,assembly_file,input_format)
        reorder_stats = mh.reorder_contigs(os.path.abspath(reference_file), assembly_file, working_dir)
        return reorder_stats ##TODO: clean up this loop  
# ##New_start is BLAST index (1, not 0)
# def reLigateCircularContig(contig,new_start,keep_forward):
#     first_start = new_start - 1 if keep_forward else new_start ##Convert to 0 index; if reverse, then identify last base in final contig
#     broken_contig = contig[first_start:] + contig[:first_start]
#     assert len(broken_contig) == len(contig), 'Reorientation changes length. Oops!'
#     final_contig = broken_contig if keep_forward else broken_contig.reverse_complement()
#     final_contig.id = contig.id+'_Reorient'
#     final_contig.name = contig.name+'_Reorient'
#     final_contig.description = contig.description+'_Reorient'
#     return final_contig
        
        
##This breaks the contig at the specified location, flips the new contgis if specified, and seals them back together if N_padding is specified
## Returns a list of contigs  
def shiftCirclarChromosome(raw_contig,new_start,reverse_contig,N_padding=-1):
    assert isinstance(raw_contig,SeqRecord.SeqRecord)
    first_start = new_start - 1 if not reverse_contig else new_start ##Convert to 0 index; if reverse, then identify last base in final contig
    if first_start in [0,len(raw_contig)]: ##Either hits first base 0 or last base in reverse direction (so index is last base + 1
        broken_contigs = [raw_contig] ##don't break
    if N_padding >= 0:
        if N_padding == 0:
            broken_contig = raw_contig[first_start:] + raw_contig[:first_start]
            print("Joining fragments with no padding")
        else:
            print("N_padding not implementing. Exiting")
            return None
        broken_contig.id += '_Reorient'
        broken_contig.name += '_Reorient'
        broken_contig.description += '_Reorient'
        broken_contigs = [broken_contig]
    else:
        broken_contigs = [raw_contig[first_start:],raw_contig[:first_start]]
        print("Leaving fragments as separate contigs")
        i = 0
        for contig in broken_contigs:
            addendum = '_Fragment_{}'.format(i)
            contig.id += addendum
            contig.name += addendum
            contig.description += addendum 
            i += 1
#     assert sum(broken_contigs) == len(contig), 'Reorientation changes length. Oops!'
    final_contigs = []
    if reverse_contig:
        final_contigs = [c.reverse_complement(id=c.id, name=c.name+'_rc', description=c.description+' (reverse complement)') for c in reversed(broken_contigs)]
    else:    
        final_contigs = broken_contigs
    assert len(raw_contig) == sum(len(contig) for contig in final_contigs), "Final contig lengths do not match original length"
    return final_contigs

##kwargs is passed to reorientation script (working_dir is primary concern right now)
def cleanupAndWrite(assembly_file,output_file,circle_new_start=None,reverse_contig=None,closed_circle=None,broken_circle=None,circularize_with_Ns=0,
                    length=None,coverage=None,report_file=None,reference=None,assembler=None,working_dir=None):
        ##Note: no sanity checks
    ## Load the assemblies
    assembly_format,assembly_compressed = utilities.guessFileFormat(assembly_file)
    output_format,output_compressed = utilities.guessFileFormat(output_file)
    if assembly_format != output_format:
        print("Warning on cleanup: input and output formats do not match ({} and {})".format(assembly_format,output_format))
    with utilities.flexible_handle(assembly_file, assembly_compressed, 'rt') as fin:
        seqs = [c for c in SeqIO.parse(fin,assembly_format)]
    #Precise manipulation of single contig
    updated_seqs = None
    if circle_new_start or reverse_contig:
        if len(seqs) > 1:
            print("Error: User provided explicit reorientation instructions for a contig, but multiple contigs are present in assembly: \n"+assembly_file)
            return 1
        elif closed_circle:
            print("Shifting closed circle...")
            updated_seqs = shiftCirclarChromosome(seqs[0],circle_new_start,reverse_contig,N_padding=0)
        elif broken_circle:
            print("Shifting broken circle...")
            updated_seqs = shiftCirclarChromosome(seqs[0],circle_new_start,reverse_contig,N_padding=-1)
        elif circularize_with_Ns > 0:
            print('Scaffolding not implemented')
        else:
            print('To shift a chromosome, you must specify whether the circle is closed or broken')
    else: ## Complex criteria for manipulation
        if closed_circle and len(seqs) > 1:
            print("Warning: Untested parameters. User specified 'closed circle' but multiple contigs are present in assembly")
    
        ## Remove the low-quality contigs:
         ##TODO: consider if another parameter should be passed. At least specify if  it came from SPAdes 
        circular = closed_circle or broken_circle##Circles imply high-quality sequence
        if not circular:
            if length is None:
                length = 0
            if coverage is None:
                coverage = 0
            if assembler is None:
                print("Removing short contigs from assembly.")
                updated_seqs = [x for x in seqs if len(x) > length]
#                 if coverage                 
            elif assembler.upper()=='SPADES':
                print("Removing low quality contigs from SPADES assembly. Length < {}; coverage < {}".format(length,coverage))
                raw_filename = os.path.join(os.path.dirname(report_file),os.path.basename(assembly_file))
                image_file = None # utilities.setExt(raw_filename, 'png') ##Note: this has been moved to the calculateStats routine
                discard_file = utilities.appendToFilename(raw_filename, '_discarded') ##ext is same as assembly file
                updated_seqs = cleanup_SPADES(seqs,minimum_length = length, minimum_coverage = coverage,export_contig_data=report_file,discard_file=discard_file,export_contig_graph=image_file)
            else:
                print("Error: assembler ({}) unknown for non-circular assembly. Not attempting to cleanup contigs in file: \n{}".format(assembler,assembly_file))
                return 1
        ## Reorient to reference if requested
        if reference:
            input_seqs = updated_seqs if updated_seqs is not None else seqs
            if os.path.isfile(reference):
                if circular:
                    if len(input_seqs) > 1:
                        print('Warning: multiple contigs in "circular" assembly. Only one contig will be reoriented and I cannot tell you which one. Untested.')  
                    if len(input_seqs) > 0:
                        N_padding = -1 ##Do not religate
                        if closed_circle:
                            N_padding=0
                        elif circularize_with_Ns > 0:
                            print('Scaffolding not implemented')
                            return 1
                        print("Reorienting circular chromosome to reference...")
                        updated_seqs = reorientClosedChromosome(input_seqs,reference,N_padding=N_padding,working_dir=working_dir) #Note: only treated as closed if N_padding >= 0
                    else: ## Len == 0
                        print("None of {} contigs passed your exclusion criteria. Exiting ".format(len(seqs)))
                        return 1
                else:
                    if working_dir is None:
                        working_dir = os.path.splitext(output_file)[0]
                    draft_name = os.path.splitext(os.path.basename(assembly_file))[0]
                    print("Reorienting contigs")
                    reorder_stats = reorientContigs(input_seqs,reference,working_dir,name=draft_name,input_format=assembly_format) ##Will be genbank format
                    if isinstance(reorder_stats,dict) and ('ReorderedDraft' in reorder_stats):
                        updated_seqs = seq_utilities.seqs_guess_and_parse2list(reorder_stats['ReorderedDraft']) ##Excessive to reload... but it fits in this flow
                    else:
                        updated_seqs = None
  
            else:
                print("Unable to realign to reference because there is no refernce file: {}".format(reference))
    if updated_seqs is None:
        print("Unable to clean and orient the assembly: \n\t"+assembly_file)
        return 1      
    else:
        with open(output_file,'wt') as fout:
            SeqIO.write(updated_seqs,fout,output_format)
        print('Saved cleaned assembly at {}'.format(output_file))
        if output_compressed:
            print("Warning. Compression not implemented. The file extension is misleading")
        return 0
     
            
            
def single(args):
    assembly_file = args.assembly
    if not os.path.isfile(assembly_file):
        print("Exiting. Unable to find file {}".format(assembly_file))
        return 1  
#     assembly_format,assembly_compressed = utilities.guessFileFormat(assembly_file)
    if args.output:
        output_file = args.output
        output_dir = os.path.dirname(output_file)
    else:
        output_dir = utilities.safeMakeOutputFolder(_outputBase)
        basename = utilities.appendToFilename(os.path.basename(assembly_file),'_RO')
        output_file = os.path.join(output_dir,basename)
    logFile = os.path.join(output_dir,"AssemblyCleanup.log")
    sys.stdout = utilities.Logger(logFile)   
    print(_outputBase)
    report_file = os.path.join(output_dir,os.path.basename(assembly_file)) + '.report.txt'
    has_out = os.path.isfile(output_file)
    has_rpt = os.path.isfile(report_file)
    if has_out or has_rpt:     
        if args.force:
            if has_out:
                print("Removing prexisting file: {}".format(output_file))
                os.remove(output_file)
            if has_rpt:
                print("Removing pre-existing file: {}".format(report_file))
                os.remove(report_file)
        else:
            print("Exiting. Refusing to overwrite pre-existing output files: \n\t{}\n\t{}".format(output_file,report_file))
            return 1
    
    try:
        open(output_file, 'a').close()
    except IOError:
        print("Exiting. Do not have permission to write to output file")
        return 1

###########Should probably be a method
    process = None
    if args.reorient:
        process = 'RO'
    elif args.discard:
        process = 'DIS'
    elif args.discard_then_reorient:
        process = 'DIS_RO'    
    else:
        print("Exiting. No processing specified")
        return(1)
    expectedArgs = set(['working_dir','report_file'])
# circle_new_start=None,reverse_contig=None,closed_circle=None,broken_circle=None,circularize_with_Ns=0,
#                     length=250,coverage=10,report_file=None,reference=None,assembler=None    
    if 'RO' in process:
        expectedArgs.update(RO_argset)
    if 'DIS' in process:
        expectedArgs.update(DIS_argset)   
        
    cleanup_args = vars(args)
    cleanup_args = {k:v for k,v in cleanup_args.items() if k in expectedArgs}
    return cleanupAndWrite(assembly_file,output_file,report_file=report_file,**cleanup_args)
    ## Load the assemblies
#     with utilities.flexible_handle(assembly_file, assembly_compressed, 'rt') as fin:
#         seqs = [c for c in SeqIO.parse(fin,assembly_format)]
    #Precise manipulation of single contig
#     cleaned = None
#     if args.circle_new_start or args.reverse_contig:
#         if len(seqs) > 1:
#             print("Exiting: User provided explicit reorientation instructions for a contig, but multiple contigs are present in assembly")
#             sys.exit(1)
#         elif args.closed_circle:
#             cleaned = shiftCirclarChromosome(seqs[0],args.circle_new_start,args.reverse_contig,N_padding=0)
#         elif args.broken_circle:
#             cleaned = shiftCirclarChromosome(seqs[0],args.circle_new_start,args.reverse_contig,N_padding=-1)
#         elif args.circularize_with_Ns > 0:
#             print('Scaffolding not implemented')
#         else:
#             print('To shift a chromosome, you must specify whether the circle is closed or broken')
#     else: ## Complex criteria for manipulation
#         if args.closed_circle and len(seqs) > 1:
#             print("Warning: Untested parameters. User specified 'closed circle' but multiple contigs are present in assembly")
#     
#         ## Remove the low-quality contigs:
#          ##TODO: consider if another parameter should be passed. At least specify if  it came from SPAdes 
#         circular = args.closed_circle or args.broken_circle##Circles imply high-quality sequence
#         cleaned = seqs if circular else cleanup_SPADES(seqs,minimum_length = args.length, minimum_coverage = args.coverage,export_contig_data=report_file)
#         ## Reorient to reference if requested
#         if args.reference:
#             if os.path.isfile(args.reference):
#                 if circular:
#                     assert len(seqs) <= 1, 'A multi-contig assembly cannot be a closed circle. This should have been caught prior to analysis'
#                     if len(seqs) == 1:
#                         N_padding = -1 ##Do not religate
#                         if args.closed_circle:
#                             N_padding=0
#                         elif args.circularize_with_Ns > 0:
#                             print('Scaffolding not implemented')
#                             sys.exit(1)
#                         cleaned = reorientClosedChromosome(cleaned,args.reference,N_padding=N_padding)
#                     else: ## Len == 0
#                         print("No {} contigs passed your exclusion criteria. Exiting ".format(len(seqs)))
#                         sys.exit(1)
#                 else:
#                 ##TODO: dump to Mauve
#                     print("Have not yet implemented multi-contig reordering. Contact developer")
#                     pass    
#             else:
#                 print("Unable to realign to reference because there is no file: ".format(args.reference))
#     if cleaned is not None:
#         with open(output_file,'wt') as fout:
#             SeqIO.write(cleaned,fout,'fasta')
#         print('Saved reoriented assembly at '+output_file)
#         return 0
#     else:
#         print("Unable to clean and orient the assembly")
#         return(1)    
req_fields = ['Filename','Gaps','Contig_Count']    
def multiple(multi_args):
    if multi_args.force and multi_args.resume:
        print("Exiting: the options 'force' and 'resume' are incompatible. Use only 'force' if you want to overwrite prior files.")
        return 1
    output_dir = multi_args.output if multi_args.output else utilities.safeMakeOutputFolder(_outputBase)
    utilities.safeMakeDir(output_dir)
    logFile = os.path.join(output_dir,"AssemblyCleanup.log")
    resultFile = os.path.join(output_dir,"AssemblyCleanupTable.tab")
    tempFile = utilities.appendToFilename(resultFile, '_temp') 
    sys.stdout = utilities.Logger(logFile)
    assembler_name = None if multi_args.assembler is None else multi_args.assembler.lower()
    print("Parameters:") 
    for k,v in vars(multi_args).items():
        print('{} : {}'.format(k,v)) 
    draft_location = multi_args.draft_location
    if os.path.isfile(draft_location):
        guideFrame = pd.read_table(draft_location)
        print('Loaded guide table from '+draft_location)
        print("\t table contains {} records".format(len(guideFrame)))
    elif os.path.isdir(draft_location):
        print("Searching for files in "+os.path.abspath(draft_location))
        deep_search = False if multi_args.shallow_search_assemblies else True     
        guideFrame = NGS_data_utilities.listGenomeFilesWithNames(draft_location,deep_search = deep_search,extension=multi_args.extension)
        ##Exclude reads
        size_limit = multi_args.size_limit
        if size_limit > 0:
            guideFrame['filesize'] = guideFrame.Filename.apply(os.path.getsize)
            small_enough = (guideFrame.filesize <= size_limit)
            if sum(small_enough) < len(guideFrame):
                print('Only {} of {} files pass the upper size limit of {}'.format(sum(small_enough),len(guideFrame),size_limit))
                guideFrame = guideFrame[small_enough].copy()
        guideFrame = guideFrame[NGS_data_utilities.dfHeaders].copy()
        if guideFrame is None or (len(guideFrame) == 0):
            print("Exiting. Failed to retrieve any files")
            return 1
        if assembler_name:
            guideFrame['assembler'] = assembler_name
            print('assigned assembler to be '+assembler_name)
        else: #This is not passed to AssemblyStats
            for i in guideFrame.index:
                if 'spades' in guideFrame.loc[i,'Filename'].lower():
                    guideFrame.loc[i,'assembler'] = 'spades' 
                    print('assigned assembler to be spades for {}'.format(guideFrame.loc[i,'Lab_ID']))        
        print('Calculating raw stats...')
        assemblyStats = AssemblyStats.calculateStats(guideFrame.Filename.tolist(),ass_format=assembler_name,image_dir=output_dir)##This will independently infer assembler from name unless given
        assemblyStats['Contig_Count'] = assemblyStats['Contig_Count'].astype(int)
        if assemblyStats is  None or len(assemblyStats) == 0:
            print("Exiting failed to calculate assembly stats on input")
            return 1
        guideFrame = pd.merge(guideFrame,assemblyStats,how='left') ##Should merge on Filename. Don't want confusion if they share other fields
        if multi_args.BCFB_PacBio_Name:
            print('interpreting BCFB PacBio names...')
            for i in guideFrame.index:
                guideFrame.loc[i,'Gaps'] = False if '.ro1m.' in guideFrame.loc[i,'Filename'] else True
        else:
            guideFrame['Gaps'] = True ### Assume no closed genomes unless stated
    else:
        print("Exiting. Unable to find the location of draft files: {}".format(draft_location))
        return(1)    
    print('Loaded data...')
    process = None
    if multi_args.reorient:
        process = 'RO'
    elif multi_args.discard:
        process = 'DIS'
    elif multi_args.discard_then_reorient:
        process = 'DIS_RO'    
    else:
        print("Exiting. No processing specified")
        return(1)
    expectedArgs = set(['working_dir','report_file','assembler'])
# circle_new_start=None,reverse_contig=None,closed_circle=None,broken_circle=None,circularize_with_Ns=0,
#                     length=250,coverage=10,report_file=None,reference=None,assembler=None    
    if 'RO' in process:
        expectedArgs.update(RO_argset)
        if not os.path.isfile(multi_args.reference):
            print("Cannot find reference file. Exiting")
            return 1
    if 'DIS' in process:
        expectedArgs.update(DIS_argset)          
    
    tag = multi_args.tag if multi_args.tag else process 
    print('Result files will have the tag "{}"'.format(tag))
        
        
    
    ##TODO test columns here
    
    permitted_fields = req_fields + list(expectedArgs)
    keep_fields = [x for x in guideFrame.columns if x in permitted_fields]
    parameterFrame = guideFrame[keep_fields].copy()
    if len(parameterFrame) == 0:
        return 1 ##Failuer
    fail_list = []
    for i,row in parameterFrame.iterrows():##Row gets converted to keyword arguments; shares index with guideFrame
        assembly_file = row['Filename']
        if not os.path.isfile(assembly_file):
            print("Error: unable to find file: {}".format(assembly_file))
            output_file = 'error. '
        else:
            print("Working on "+os.path.basename(assembly_file))
            print("\tat  {}".format(time.ctime()))
            del row['Filename']
            if 'Contig_Count' in row.index:
                if (str(row['Contig_Count']) == str(1)):
                    gaps = row['Gaps']
                    gap_bool = True ##Safest default (will introduce contig breaks). But should probably skip reorientation
                    if isinstance(gaps,str):
                        if gaps.upper() == 'TRUE':
                            gap_bool = True
                        elif gaps.upper() == 'FALSE':
                            gap_bool = False
                        else:
                            print("unable to interpret 'gaps' notation: {}".format(gaps))
                            continue
                    elif isinstance(gaps,bool):
                        gap_bool = gaps
                    else:
                        print("unable to interpret 'gaps' notation: {}".format(gaps))
                        continue
                    if gap_bool:
                        row['broken_circle'] = True ##NOTE: with our bacteria, we assume circle
                    else:
                        row['closed_circle'] = True
                        
                del row['Gaps']
                    
            assembly_basename = utilities.appendToFilename(os.path.basename(assembly_file),'_'+tag)
            output_file = os.path.join(output_dir,assembly_basename)
            
            report_file = os.path.join(output_dir,os.path.basename(assembly_file)) + '.report.txt'
            has_out = os.path.isfile(output_file)
            has_rpt = os.path.isfile(report_file)
            if has_out or has_rpt:
                if multi_args.force:
                    if has_out:
                        print("Removing prexisting file: {}".format(output_file))
                        os.remove(output_file)
                    if has_rpt:
                        print("Removing pre-existing file: {}".format(report_file))
                        os.remove(report_file)
                else:
                    if not multi_args.resume:
                        print("Error: Refusing to overwrite pre-existing output files: \n\t{}\n\t{}".format(output_file,report_file))
                    continue
            try:
                open(output_file, 'a').close()
                os.remove(output_file) 
            except IOError:
                print("Error. Do not have permission to write to output file \n\t{}".format(output_file))
                continue
            
            cleanup_args = vars(multi_args).copy() ##TODO: put this up front?
            cleanup_args.update(row.to_dict())    
            cleanup_args['working_dir'] = os.path.join(output_dir,'work') 
            cleanup_args = {k:v for k,v in cleanup_args.items() if k in expectedArgs}
            if 'Mean_Coverage' in row.index:
                proportion_cutoff = multi_args.coverage_proportion * row.loc['Mean_Coverage']
                min_coverage = max(multi_args.coverage,proportion_cutoff)
                cleanup_args['coverage'] = min_coverage
                del cleanup_args['Mean_Coverage']
            else:
                cleanup_args['coverage'] = multi_args.coverage ##This should actually be irrelevant -- 
            try:    
                print("Arguments:")
                print(cleanup_args)
                if cleanupAndWrite(assembly_file,output_file,report_file=report_file,**cleanup_args) != 0: ##TODO: return stats
                    output_file = 'error'
                    fail_list.append(assembly_file)
            except Exception as e:
                fail_list.append(assembly_file)
                output_file = 'error'
                warn="Exception on cleanupAndWrite:"
                utilities.printExceptionDetails(e,warn)
            print() ##Blank line
        guideFrame.loc[i,'CleanedFile'] = output_file
        guideFrame.to_csv(tempFile,index=False,sep='\t')
    print("Errors on {} files: ".format(len(fail_list)))
    print("\n\t".join(fail_list))
    if process in ['DIS','DIS_RO']: ##recalculate stats for filtered contig sets
        assemblyStats2 = AssemblyStats.calculateStats(guideFrame.CleanedFile.tolist(),ass_format=assembler_name)
        if assemblyStats2 is not None:
#             assemblyStats2.rename(columns={'Filename':'CleanedFile'},inplace=True)
            guideFrame = AssemblyStats.BeforeAndAfter(guideFrame.set_index("CleanedFile"),assemblyStats2.set_index('Filename'))
#             guideFrame = pd.merge(guideFrame,assemblyStats2,on='CleanedFile',suffixes=('_raw',''),how='outer')
    print("Reporting stats for {} genomes.".format(len(guideFrame)))
    guideFrame.fillna('N/A', inplace=True)
    utilities.safeOverwriteTable(resultFile, guideFrame, 'tab',index=False)     
    return 0
#     else:
#         return 1 ##Absence of assembly stats frame indicates failure to generate files
            
    #         assembly_file,output_file,circle_new_start=None,reverse_contig=None,closed_circle=None,broken_circle=None,circularize_with_Ns=0,
    #                     length=250,coverage=10,report_file=None,reference=None
    # 
    #         ## Load the assemblies
    #         assembly_format,assembly_compressed = utilities.guessFileFormat(assembly_file)
    #         with utilities.flexible_handle(assembly_file, assembly_compressed, 'rt') as fin:
    #             seqs = [c for c in SeqIO.parse(fin,assembly_format)]
    #         #Precise manipulation of single contig
    #         cleaned = None
    #         if args.circle_new_start or args.reverse_contig:
    #             if len(seqs) > 1:
    #                 print("Exiting: User provided explicit reorientation instructions for a contig, but multiple contigs are present in assembly")
    #                 sys.exit(1)
    #             elif args.closed_circle:
    #                 cleaned = shiftCirclarChromosome(seqs[0],args.circle_new_start,args.reverse_contig,N_padding=0)
    #             elif args.broken_circle:
    #                 cleaned = shiftCirclarChromosome(seqs[0],args.circle_new_start,args.reverse_contig,N_padding=-1)
    #             elif args.circularize_with_Ns > 0:
    #                 print('Scaffolding not implemented')
    #             else:
    #                 print('To shift a chromosome, you must specify whether the circle is closed or broken')
    #         else: ## Complex criteria for manipulation
    #             if args.closed_circle and len(seqs) > 1:
    #                 print("Warning: Untested parameters. User specified 'closed circle' but multiple contigs are present in assembly")
    #         
    #             ## Remove the low-quality contigs:
    #              ##TODO: consider if another parameter should be passed. At least specify if  it came from SPAdes 
    #             circular = args.closed_circle or args.broken_circle##Circles imply high-quality sequence
    #             cleaned = seqs if circular else cleanup_SPADES(seqs,minimum_length = args.length, minimum_coverage = args.coverage,export_contig_data=report_file)
    #             ## Reorient to reference if requested
    #             if args.reference:
    #                 if os.path.isfile(args.reference):
    #                     if circular:
    #                         assert len(seqs) <= 1, 'A multi-contig assembly cannot be a closed circle. This should have been caught prior to analysis'
    #                         if len(seqs) == 1:
    #                             N_padding = -1 ##Do not religate
    #                             if args.closed_circle:
    #                                 N_padding=0
    #                             elif args.circularize_with_Ns > 0:
    #                                 print('Scaffolding not implemented')
    #                                 sys.exit(1)
    #                             cleaned = reorientClosedChromosome(cleaned,args.reference,N_padding=N_padding)
    #                         else: ## Len == 0
    #                             print("No {} contigs passed your exclusion criteria. Exiting ".format(len(seqs)))
    #                             sys.exit(1)
    #                     else:
    #                     ##TODO: dump to Mauve
    #                         print("Have not yet implemented multi-contig reordering. Contact developer")
    #                         pass    
    #                 else:
    #                     print("Unable to realign to reference because there is no file: ".format(args.reference))
    #         if cleaned is not None:
    #             with open(output_file,'wt') as fout:
    #                 SeqIO.write(cleaned,fout,'fasta')
    #             print('Saved reoriented assembly at '+output_file)
    #         else:
    #             print("Unable to clean and orient the assembly")
    #             return(1)               
    
    
import argparse        
def main():
    print("")
    print("Running {} from {} at {}".format(SCRIPT_NAME,os.getcwd(),time.ctime()))
    print("...script is found in {}\n".format(SCRIPT_DIR)) 
    
    parser = argparse.ArgumentParser(description='A program to select and reorder decent contigs in genome assemblies (especially from SPADES).')
    ##Info
    process_group = parser.add_argument_group(title='processes',description="Choose at least one process to apply to the genomes. Defaults to 'discard' behavior")
    process_group.add_argument('--reorient',action='store_true',help="Reorient genomes according to a reference")
    process_group.add_argument('--discard',action='store_true',help="Discard low value contigs (based on length and coverage)")
    process_group.add_argument('--discard_then_reorient',action='store_true',help='First discard low value contigs, then reorient according to reference')
    parser.add_argument('--force','-f',action='store_true',help='Force overwrite of output')
    parser.add_argument('--version','-V',action='version',version='%(prog)s {}'.format(SCRIPT_VERSION))
    parser.add_argument('--circularize_with_Ns',type=int,default=0,help='Assume that contigs are circular and add this many Ns to fill circle. Default is to leave contig broken')
    parser.add_argument('--reference','-r',help="Reference genome for contig reordering")
    parser.add_argument('--coverage','-c',help='Minimum coverage to keep contig (extracted from SPADES contig description) (will use maximum of coverage and coverage_proportion)',default=5,type=int)
    parser.add_argument('--coverage_proportion','-p',type=float,help='Minimum coverage to to keep contig, as proportion of genome-wide mean.  (will use maximum of coverage and coverage_proportion)',default=0)
    parser.add_argument('--length','-l',help='Minimum length to keep contig',default=250,type=int)
    parser.add_argument('--assembler','-a',help="Assembler used to produce contigs (e.g. SPADES). Provides description of read coverage for cleaning")
#     parser.add_argument('--debug',action='store_true',help='Create a temporary repository in current directory')
    subparsers = parser.add_subparsers(title='subcommands',
                                        description='valid subcommands',
                                        help='additional help')
    single_ass = subparsers.add_parser('single')
    single_ass.set_defaults(func=single)
    single_ass.add_argument('assembly',help='assembly FASTA file to reorder')
    single_ass.add_argument('--output','-o',help='File to write processed assembly. Default is '+_outputBase)
    single_ass.add_argument('--closed_circle',action='store_true',help='The assembly is a closed, circular contig')
    single_ass.add_argument('--broken_circle',action='store_true',help='The assembly in in a single contig, but was not closed')
    single_ass.add_argument('--circle_new_start','-c',type=int,help='New start position for single circular contig in assembly file')
    single_ass.add_argument('--reverse_contig',action='store_true',help='Reverse the single contig in assembly file')
    
    multi_ass = subparsers.add_parser('multiple')
    multi_ass.set_defaults(func=multiple)
    multi_ass.add_argument('draft_location',help='Either a directory containing files to reorder or a table with required fields: {}'.format(', '.join(req_fields)))
    multi_ass.add_argument('--output','-o',help='Directory to write processed assemblies. Default is '+_outputBase)
    multi_ass.add_argument('--resume',action='store_true',help='Suppresses error messages when result files are found in output directory.')
    multi_ass.add_argument('--tag','-t',help='Tag to append to filenames, indicating whether they have been reoriented (RO by default) or cleaned (CL) ')
    multi_ass.add_argument('--shallow_search_assemblies',help='If drafts are in a folder, do not search subdirectories for assemblies',action='store_true')
    multi_ass.add_argument('--BCFB_PacBio_Name',help='Files are named with BCFB PacBio conventions (".ro1m." means circularized)',action='store_true')
    multi_ass.add_argument('--extension','-e',help='Limit search to files with this extension')
    multi_ass.add_argument('--size_limit','-s',help='Limit on the size of files to analyze, in bytes (e.g. to exclude read data). Set to 0 to inactivate',default=25000000,type=int)


    ##TODO: option to break a contig to reorder?
    
    ### Check the import and export locations
    args = parser.parse_args()
    
    
    ##Establish shared settings
    
    
    ##Run program
        ##Run the program
    result = args.func(args)
    if result != 0:
        parser.print_usage()
        
    
        
    


if __name__ == "__main__":
    if not utilities.has_preferred_python():
        raise Exception("Upgrade your python version")
    main()        
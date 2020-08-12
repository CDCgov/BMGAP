#! /bin/env python3
### 
##by Adam Retchless
## Mar 3, 2016, 
SCRIPT_VERSION = 1
SCRIPT_SUBVERSION = 8 ##proportion coverage


#pylint: disable=global-statement, broad-except
from Bio import SeqIO
import os
import pandas as pd
import time
import utilities
import seq_utilities
import AssemblyStats
# has_plt = False
# try:
#     import matplotlib.pyplot as plt
#     has_plt = True
# except ImportError:
#     print("Cannot produce plots without the pyhon module 'matplotlib'")

script_base = os.path.basename(__file__)
_outputBase = '{}_v{}.{}'.format(os.path.splitext(script_base)[0],SCRIPT_VERSION,SCRIPT_SUBVERSION)

my_file = __file__
if os.path.islink(my_file):
    my_file = os.path.realpath(my_file)
SCRIPT_DIR, SCRIPT_NAME = os.path.split(my_file)
SCRIPT_DIR = os.path.abspath(SCRIPT_DIR)

ContigHeaders = ['Contig_ID','Length','Coverage','Contig']
DIS_argset = set(['length','coverage','assembler'])

def cleanup_SKESA(contigs,minimum_length, minimum_coverage, export_contig_data=None,discard_file=None,export_contig_graph=None):
    contig_table = AssemblyStats.parse_SKESA(contigs,export_contig_graph=export_contig_graph,export_contig_data=export_contig_data)
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

##kwargs is passed to reorientation script (working_dir is primary concern right now)
def cleanupAndWrite(assembly_file,output_file,length=None,coverage=None,image_file=None,base_ID=None):
        ##Note: no sanity checks
    ## Load the assemblies
    assembly_format,assembly_compressed = utilities.guessFileFormat(assembly_file)
    output_format,output_compressed = utilities.guessFileFormat(output_file)
    if assembly_format != output_format:
        print("Warning on cleanup: input and output formats do not match ({} and {})".format(assembly_format,output_format))
    with utilities.flexible_handle(assembly_file, assembly_compressed, 'rt') as fin:
        seqs = [c for c in SeqIO.parse(fin,assembly_format)]
    if base_ID is not None:
        new_contigs, c = seq_utilities.standardize_contig_names(seqs,base_ID)
        seqs = new_contigs
    #Precise manipulation of single contig
    if length is None:
        length = 0
    if coverage is None:
        coverage = 0
    ##always SPADES
    print("Removing low quality contigs from SKESA assembly. Length < {}; coverage < {}".format(length,coverage))
#     raw_filename = os.path.join(os.path.dirname(report_file),os.path.basename(assembly_file))
    discard_file = utilities.appendToFilename(output_file, '_discarded') ##ext is same as assembly file
    updated_seqs = cleanup_SKESA(seqs,minimum_length = length, minimum_coverage = coverage,discard_file=discard_file,export_contig_graph=image_file)
    if updated_seqs is None:
        print("Unable to clean and orient the assembly: \n\t"+assembly_file)
        return 1      
    else:
        print("Retained {} of {} contigs.".format(len(updated_seqs),len(seqs)))
        with open(output_file,'wt') as fout:
            SeqIO.write(updated_seqs,fout,output_format)
        print('Saved reoriented assembly at {}'.format(output_file))
        if output_compressed:
            print("Warning. Compression not implemented. The file extension is misleading")
        return 0
    

import argparse        
def main():
    print("")
    print("Running {} from {} at {}".format(_outputBase,os.getcwd(),time.ctime()))
    print("...script is found in {}\n".format(SCRIPT_DIR)) 
    
    parser = argparse.ArgumentParser(description='A program to select and reorder decent contigs in genome assemblies (especially from SPADES).')
    ##Info
    parser.add_argument('--version','-V',action='version',version='%(prog)s {}'.format(SCRIPT_VERSION))
    parser.add_argument('--coverage','-c',help='Minimum coverage to keep contig (extracted from SPADES contig description)',default=0,type=int)
    parser.add_argument('--coverage_proportion','-p',type=float,help='Minimum coverage to to keep contig, as proportion of genome-wide mean.  (will use maximum of coverage and coverage_proportion)',default=0)
    parser.add_argument('--length','-l',help='Minimum length to keep contig',default=250,type=int)
    parser.add_argument('--base_ID','-b',help='Identifier for the assembly. Will be added as prefix for all contigs.')
#     parser.add_argument('--assembler','-a',help="Assembler used to produce contigs (e.g. SPADES). Provides description of read coverage for cleaning")
    parser.add_argument('assembly',help='assembly FASTA file to discard from')  
    parser.add_argument('output',help='File to write processed assembly') 
    
    args = parser.parse_args()
    
    assembly_file = args.assembly
    if not os.path.isfile(assembly_file):
        print("Exiting. Unable to find file {}".format(assembly_file))
        return 1  
#     assembly_format,assembly_compressed = utilities.guessFileFormat(assembly_file)
    print("Parameters:") 
    for k,v in vars(args).items():
        print('{} : {}'.format(k,v)) 
    output_file = args.output
    report_file = output_file + '.report.tab'
    has_out = os.path.isfile(output_file)
    has_rpt = os.path.isfile(report_file)
    if has_out or has_rpt:     
        print("Exiting. Refusing to overwrite pre-existing output files: \n\t{}\n\t{}".format(output_file,report_file))
        return 1
    else:
        print("Output files look good")
    try:
        open(output_file, 'a').close()
        os.remove(output_file)
        print("Tested ability to print. Success")
    except IOError:
        print("Exiting. Do not have permission to write to output file")
        return 1
    try:
        image_file = utilities.setExt(report_file, 'png') ##Note: this has been moved to the calculateStats routine
        print("Calculating assembly stats")
        pre_stats = AssemblyStats.calculateStats([assembly_file],ass_format='skesa')
        proportion_cutoff = args.coverage_proportion * pre_stats.loc[0,'Mean_Coverage']
        min_coverage = max(args.coverage,proportion_cutoff)
        print("Removing suprious contigs")
        cleanupAndWrite(assembly_file,output_file,image_file=image_file,length=args.length,coverage=min_coverage,base_ID=args.base_ID)
        print("Calculating clean assembly stats")        
        post_stats = AssemblyStats.calculateStats([output_file],ass_format='skesa')
        print("Formatting assembly stats for printing") 
        merged_stats = AssemblyStats.BeforeAndAfter(pre_stats,post_stats)
        merged_stats.to_csv(report_file,sep='\t',index=False)
    except (ValueError, IOError) as e:
        print(e)
        parser.print_usage()
    
    
if __name__ == "__main__":
    if not utilities.has_preferred_python():
        raise Exception("Upgrade your python version")
    main()

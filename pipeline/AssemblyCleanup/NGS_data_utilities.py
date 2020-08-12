###These utility functions crawl though directories to find NGS data files, identify my labortory identifier (M#) and connect them.
## Type -h to see usage
import utilities
import re
import os, sys
from collections import defaultdict
import pandas as pd
import time
import itertools

SCRIPT_VERSION = 1 #Updatinng "listReadsWithFilename" to handle shallow shearch and report realpath
SCRIPT_SUBVERSION =  17#external stuff

script_base = os.path.basename(__file__)
_outputBase = '{}_v{}.{}'.format(os.path.splitext(script_base)[0],SCRIPT_VERSION,SCRIPT_SUBVERSION)
default_logfile = os.path.splitext(script_base)[0]+'.log'

dfHeaders = ['Lab_ID','Filename']
read_ext = '.fastq.gz'
motif_ext = '.motif_summary.csv'
sam_ext = ['.sam','.bam']
read_data_fileHeaders = ['Lane','Sample ID','Index','Yield (Mbases)','# Reads','% Perfect Index Reads','% of >= Q30 Bases (PF)','Mean Quality Score (PF)']

default_ass_dir = '/scicomp/groups/OID/NCIRD/DBD/MVPDB/ML/data/BCFB/by-project/'
default_read_dir = '/scicomp/groups/OID/NCIRD/DBD/MVPDB/ML/data/BCFB/by-instrument/'
default_read_mirror = '/scicomp/groups/OID/NCIRD/DBD/MVPDB/ML/share/out/ncbs/BCFB_mirror/by-instrument/'
external_read_mirror = '/scicomp/groups/OID/NCIRD/DBD/MVPDB/ML/share/out/ncbs/external_IlluminaData'
BML_read_locations = ['/scicomp/instruments/18-1-218_Illumina-MiSeq-M03282/',
                      '/scicomp/instruments/18-1-218_Illumina-MiSeq-M04832/']
default_NCBS_dir = '/scicomp/groups/OID/NCIRD/DBD/MVPDB/ML/share/in/ncbs/Assemblies'

default_misname_file = '/scicomp/groups/OID/NCIRD/DBD/MVPDB/ML/standard_analysis/mislabeled_sequences/Mislabeled_Sequences.xlsx'##May have a date in there

reads_file = 'BCFB_raw_instrument_reads.tab'
assemblies_file = 'BCFB_raw_project_assemblies.tab'
MiSeq_files = 'BML_MiSeq_reads.tab'
mirrored_reads = 'BCFB_mirrored_forNCBS.tab'
# NCBS_processed = 'NCBS_reads_assemblies.tab'


GWA = '/scicomp/groups/OID/NCIRD/DBD/MVPDB/ML/'
##This will follow links (top-down) to get the real path to the filename, but will not leave the target_path if it is currently on the target path 
## The default should cause it to act like "real path" (just follow all links, since all start with target path)
def onTarget(path,target):
    return target.startswith(path) or path.startswith(target)

def stayOnPath(filename,target_path='/'):
    filepath = os.path.abspath(filename) ##not real path
    path_parts = filepath.split('/')
    path_new = '/'
    for p in path_parts:
        if p != '':
            path_new = os.path.join(path_new,p)
            if os.path.islink(path_new):
#                 print("Found link: "+path_new)
#                 print("taraget: "+target_path)
#                 print("old path: "path_new)

                temp_path = os.path.abspath(os.readlink(path_new)) ##Abspath, not real path
                if onTarget(temp_path,target_path) or not onTarget(path_new,target_path):
                    path_new = temp_path
    return path_new




##Looks for a Meningitis lab sample identifier (M#) in the filename. Currently uses the strict definition ("M" plus 5 digits).
# Returns empty string if fails

########## Transferred to NGS_data_utilities ########################
getName = re.compile(r'(M\d{5})') #Identifying Lab ID  ##Note: some samples concievably use a different pattern
def guessNameFromGenomeFile(filename,fallback=False):
    sample_name = ''
    basename = os.path.basename(filename)
    nameMatch = getName.match(basename) ## Need to specify that ID is at beginning of file. There's risk of MiSeq machine names being in filename too -- with same format
    if nameMatch:
        sample_name = nameMatch.group()
    if (sample_name == '') and fallback:
        sample_name = '_'.join(basename.split('_')[:-4]) ##Cut off the last 4 sections of the illumina file format
        if sample_name == '':
            sample_name = basename.split('.')[0] ##Take everything
    return sample_name

def assignUniqueID(df):
    df['Unique_ID'] = df['Lab_ID']
    i = 0
    while sum(df['Unique_ID'].duplicated()) > 0:
        df.loc[df['Unique_ID'].duplicated(),'Unique_ID'] = df['Unique_ID']+'r'+str(i)# pylint: disable=no-member
        i+=1    

def listGenomeFilesWithNames(directory,outfile = None, deep_search = True, verbose = False, extension =None,target_path = '/',sample_is_first=False):
    ##Create Regex to identify sequence files, based on extensions
    extSet = set(utilities.format_guesser.keys())
    rePattern = r'('
    append_or = False
    if isinstance(extension,str):
        rePattern += re.escape(extension)
    else:
        for ext in extSet:
            if append_or:
                rePattern += "|"
            else: ##Only first one does not need the operator
                append_or = True
            rePattern += re.escape(ext)
    rePattern += ')(.gz)?$'
    extRE = re.compile(rePattern)
    #~ if _verbose: print("Calling listGenomeFilesWithNames with options {} and {} and {}".format(directory,outfile,extPatterns))
    ##Source directory has two FASTA files for each genome -- the name on one says if it is a complete chromosome; other has jobID
    fileList = []
    fail = 0
    df = None
    ##Find all read files in this directory tree
    search_dir = os.path.abspath(directory)
    if deep_search:
        for rootdir, _, files in os.walk(search_dir):
            first_file = True
            for filename in files: ##TODO refactor
                if extRE.search(filename):
                    if first_file:
                        if verbose:
                            print("\t Collecting files from directory: "+rootdir)
                        first_file = False
                    fileList.append(os.path.join(rootdir,filename))
                else:
                    if verbose:
                        print("ignoring file: "+filename)
    else:
        all_files = os.listdir(search_dir)
        first_file = True
        for filename in all_files: ##TODO refactor
            if extRE.search(filename):
                if first_file:
                    print("\t Collecting files from directory: "+search_dir) 
                    first_file = False
                fileList.append(os.path.join(search_dir,filename))
            else:
                if verbose:
                    print("ignoring file: "+filename)        
#     for filename in os.listdir(directory):
#         if extRE.search(filename):
#             fileList.append(os.path.join(directory,filename))
#         else:
#             if _verbose: print("ignoring file: "+filename)
    if len(fileList) > 0:
        genomeList = []
        for filename in fileList:
            sample_name = guessNameFromGenomeFile(filename) ##default is ''
#             if _verbose: print('File: {} \n Sample: {}'.format(filename,sample_name))
            if sample_name == '':
                if sample_is_first: 
                    fail += 1
                    sample_name = os.path.basename(filename).split('_')[0]
                else:
                    fail += 1
                    sample_name = 'Assembly-{}'.format(fail)
            genomeList.append([sample_name,stayOnPath(filename,target_path)])
        if len(genomeList) > 0:
            df = pd.DataFrame(genomeList,columns = dfHeaders)
            df_trim = df[df['Lab_ID'] != '']
            if len(df_trim) > 0:
                g = df_trim.groupby('Lab_ID')
                unique = len(g)
                print("Found {} sequence files in {}.\n Failed to identify names for {}.\n There were {} unique names".format(len(fileList),directory,fail,unique))
            else:
                print("Could not find any sample identifiers")
            df.sort_values('Lab_ID') 
            ##TODO merge
            if outfile is not None:
                genomeFrame = None ##Append to exsiting directory file if it exists
                if os.path.isfile(outfile):
                    genomeFrame = pd.read_table(outfile) 
                    print("Appending genome list to existing file: "+outfile)
                    #~ genomeFrame.append(df,ignore_index=True)
                    genomeFrame = pd.concat([genomeFrame,df],ignore_index=True)
                else:
                    genomeFrame = df
                    print("Saving list to "+outfile)
                    ##ToDo: I should validate that 
                genomeFrame.to_csv(outfile,sep='\t',index=False)
#             fileSizes = df.Filename.apply(os.path.getsize)
        #     print("Total file sizes: {}".format(sum(fileSizes)))
        #     print("Minimum file size: {}".format(min(fileSizes.tolist())))
            fileSizeZero = df.Filename.apply(os.path.getsize) == 0
            if sum(fileSizeZero) > 0:
                print("Removing {} genome files with size 0".format(sum(fileSizeZero)))
                df = df[~fileSizeZero].copy()
                print("Keeping {} genome files.".format(len(df)))   
            df['Date_Assembly_Created'] = df.Filename.apply(lambda x : time.ctime(os.path.getctime(x)))                
                       
        else:
            print("Failed to identify files in directory {}".format(directory))
    else:
        print("Failed to identify files using following search string: "+rePattern)

    return df

##Copy the assembly file to a new location, with a simple name and simple contig identifiers    
### Try to keep the same contig ID numbers and keep them in the same order in the file
subpath = 'Data/Intensities/BaseCalls'
def extractMiSeqDirectory(MiSeq_dir,read_extension=None,verbose=False,doAssignReadSets=False):
    df = None    
    if isinstance(MiSeq_dir,str) and os.path.isdir(MiSeq_dir):
        data_dir = os.path.join(MiSeq_dir,subpath)
        print(data_dir)
        if os.path.isdir(data_dir):
            df = matchReadFilesToSampleSheet(data_dir, read_extension=read_extension, verbose=verbose, doAssignReadSets=doAssignReadSets)
            if df is None: ##No sample sheet; just report reads
                df = listReadFilesWithNames(data_dir, read_extension=read_extension, verbose=verbose, doAssignReadSets=doAssignReadSets,deep_search=False)
        else:
            print("Cannot find data directory: "+data_dir)
    return df
    
def listReadsFromMiSeqToplevel(directories,outfile = None,read_extension=None,verbose=False,doAssignReadSets=False, dirValidate = True):
    
    if isinstance(directories,str):
        directory_locations = [directories] 
    else:
        directory_locations = [d for d in directories if os.path.isdir(d)]
        if len(directory_locations) < len(directories):
            print("##")
            print("Warning: unable to location all search directories")
            print('\t'+','.join([d for d in directories if d not in directory_locations]))       
    readFrame = None ##Append to existing directory file if it exists    
    directory_list = [os.path.join(d,x) for d in directory_locations for x in os.listdir(d) if os.path.isdir(os.path.join(d,x))]
    dirs = {}
    print("Directories: {}".format(len(directory_list)))
    df = None
    for d in directory_list:
        temp = extractMiSeqDirectory(d,read_extension=read_extension,verbose=verbose,doAssignReadSets=doAssignReadSets)
        if temp is not None:
            if df is None:
                df = temp
            else:
                df = df.append(temp)
            if 'Sample_Name' in temp.columns:
                dirs[d] = '({} samples)'.format(len(temp))
            else:
                dirs[d] = '({} samples -- no sheet)'.format(len(temp))
        else:
            dirs[d] = '(empty)'
    if df is None:
        print("Failed to identify any reads in any MiSeq directory: "+','.join(directory_list))
    elif outfile is not None:
        df.rename(columns={'Date_Ingested':'Date_Documented'},inplace=True)
        if os.path.isfile(outfile):
            readFrame = pd.read_table(outfile) 
            print("Appending read list to existing file: "+outfile)
            readFrame = pd.concat([readFrame,df],ignore_index=True)
        else:
            readFrame = df
            print("Saving list to "+outfile)
        readFrame.dropna(axis=1,how='all',inplace=True)
        readFrame.set_index('Lab_ID').to_csv(outfile,sep='\t')
        if dirValidate:
            directory_list.sort()
            empty_file = utilities.appendToFilename(outfile, "_empty_dirs")
            with open(empty_file,'wt') as fout:
                for d in directory_list:
                    line_out = dirs[d]+": "+d 
                    print(line_out,file=fout)  
                
    return readFrame
        
## Need a way to match up the unpaired read files that arise from filtering of reads
## outfile saved as tab-delimited
samplesheet = "SampleSheet.csv"
from io import StringIO
def matchReadFilesToSampleSheet(directory,outfile = None,read_extension=None,verbose=False,doAssignReadSets=False):
    pid = 'Sample_Number' #This is returned by listReadsWithNames
    ss_file = os.path.join(directory,samplesheet)
    result = None
    if os.path.isfile(ss_file):
        ##Note, this will only work for reads that use our sample names
        readFrame = listReadFilesWithNames(directory, None, read_extension, verbose, doAssignReadSets,deep_search=False,useLabID=False)
        if isinstance(readFrame,pd.DataFrame):
            readFrame = readFrame[['Lab_ID', 'Sample','Sample_Number','Read1', 'Read2', 'Date_Created', 'Date_Ingested']].copy()   
#             print(readFrame['Set'])
#             readFrame[pid] = readFrame['Sample_Number']#.apply(os.path.basename).str.split('_').str.get(1) ##     
            sio = StringIO()
            read = False
            with open(ss_file) as ss_in:
                for l in ss_in:
                    if read:
                        sio.write(l)
                    else:
                        read = l.startswith('[Data]')
            sio.seek(0)
            samples = pd.read_csv(sio)
            samples.dropna(subset=['Sample_ID'],inplace=True) #TODO: limit this to sample_ID ... and change stuff below to make sample_name optional (for generalization)
            samples.reset_index(drop=True)
            print("Read {} items from sample sheet".format(len(samples)))
            if len(samples) > 0:  ##All real samples should have a name
    #             samples['Lab_ID'] = samples['Sample_Name'].str.split("_").str.get(0)
                samples['Sample_Name'] = samples['Sample_Name'].fillna('')
                samples['Sample'] = samples['Sample_Name'].str.replace("_",'-') #This is the first field in the MiSeq filename
                samples['LIMS_ID'] = samples['Sample_ID'].str.split("_").str.get(1)          
                samples[pid] = None
                for x in samples.index:
                    samples.loc[x,pid] = 'S{}'.format(x + 1)             
                result = pd.merge(samples,readFrame,how='left',on=['Sample',pid])
                if len(result) == 0:
                    print("Error, could not merge sample sheet with reads")
                    print("Sample frame:")
                    print(samples)
                    print("Read frame:")
                    print(readFrame)
                    result = None
                else:
                    
        #             print(result.columns)
        #             print(result[['ExpectedID','Read1']])
                    if sum(result.apply(lambda x : x.loc[pid] in os.path.basename(str(x.loc['Read1'])),axis=1)) != len(result):
                        print("Failed to match files to samples sheet in "+directory)
                        result = None
                if result is None:
                    print("Merging on sample name and LIMS_ID, not sample number")
                    samples.rename(columns={pid:pid+'_SampleSheet'},inplace=True)
#                     samples['Sample'] = samples['Sample_Name'].str.replace("_",'-')
                    readFrame['LIMS_ID'] = readFrame['Sample'].str.replace("-",'_').str.split("_").str.get(1)
                    result = pd.merge(samples,readFrame,how='left',on=['Sample',"LIMS_ID"])
                    if len(result) == 0:
                        print("Error, could not merge sample sheet with reads")
                        print("Sample frame:")
                        print(samples)
                        print("Read frame:")
                        print(readFrame)
                        result = None
                    else:
                        
            #             print(result.columns)
            #             print(result[['ExpectedID','Read1']])
                        if sum(result.apply(lambda x : isinstance(x,str) and x.loc[pid] in os.path.basename(str(x.loc['Read1'])),axis=1)) != len(result):
                            print("Failed to match files to samples sheet in "+directory)
                            result = None                         
            
#     else:
#         result = readFrame
    if isinstance(result,pd.DataFrame) and (outfile is not None):
        utilities.safeOverwriteTable(outfile, result, 'tab')
    return result
    
    
##Returns NONE if no files found
r1 = 'R1'
r2 = 'R2'
df_read_codes = [r1,r2]
def listReadFilesWithNames(directory,outfile = None,read_extension=None,verbose=False,doAssignReadSets=False, deep_search = True,read_codes=None,useLabID=True,target_path='/'):
    if read_codes is None:
        read_codes = df_read_codes
    if read_extension is None:
        read_extension = read_ext
    extRE = re.compile(re.escape(read_extension)) #All read files are compressed fastq
    fileList = []
    readDataFile = None
    ##Find all read files in this directory tree
    abs_dir = stayOnPath(directory,target_path)
    print("Directory is "+abs_dir)
    if deep_search:
        for rootdir, _, files in os.walk(abs_dir):
            if verbose: 
                print("Scanning {}".format(rootdir))
            for filename in files:
                if extRE.search(filename):
                    fileList.append(stayOnPath((os.path.join(rootdir,filename)),target_path))
                else:
                    if (rootdir == abs_dir) and (filename.endswith('.xlsx') and (not filename.startswith('~'))):
                        if readDataFile is None:
                            readDataFile = os.path.join(abs_dir,filename)
                        else:
                            print("Warning: found multiple excel files in top of directory. Not clear which is the demultiplexing file")
                    if verbose: 
                        print("ignoring file: "+filename)
    else:
        all_files = os.listdir(abs_dir)
        first_file = True
        for filename in all_files: ##TODO refactor
            if extRE.search(filename):
                if first_file:
                    print("\t Collecting files from directory: "+abs_dir) 
                    first_file = False
                fileList.append(os.path.join(abs_dir,filename))
            else:
                if verbose:
                    print("ignoring file: "+filename)   
                      

    if verbose: print("Identified {} files in {}".format(len(fileList),directory))
    #### Interpret the read filenames
    readFrame =  pairReads(fileList,read_codes=read_codes,useLabID=useLabID)    
    #### Append any additional information
    if readFrame is None:
        print("Failed to identify read files in {}".format(directory))
    else:
        try:
            readFrame['Date_Created'] = readFrame['Read1'].apply(lambda x : time.ctime(os.path.getctime(x)))
        except OSError as e:
            print("Failure to identify file creation times")
            utilities.printExceptionDetails(e)
        readFrame['Date_Ingested'] = time.ctime()
        if verbose: print("Returned {} read sets".format(len(readFrame)))
        if readDataFile is not None: ###Append data to frame if available; filename is identified during directory search,  so file exists
            readDataFrame = openReadDataFile(readDataFile)
            if isinstance(readDataFrame,pd.DataFrame):
                readFrame = pd.merge(readFrame,readDataFrame,how='left')
            else:
                print("Error reading read data file")
        if outfile is not None:
            if os.path.isfile(outfile):
                priorFrame = pd.read_table(outfile) 
                print("Appending read list to existing file: "+outfile)
                #~ genomeFrame.append(df,ignore_index=True)
                totalFrame = pd.concat([priorFrame,readFrame],ignore_index=True)
            else:
                totalFrame = readFrame
                print("Saving list to "+outfile)
                ##ToDo: I should validate that 
            totalFrame.to_csv(outfile,sep='\t',index=False)
    if doAssignReadSets:
        assignReadSets(readFrame)
    return readFrame

## Input is the 
def assignReadSets(readFrame,useSampleLane=True):
    if isinstance(readFrame,pd.DataFrame):
        for _,g in readFrame.groupby('Lab_ID'):
            c = 0
            for i in g.index:
                readset = ''
                sample = readFrame.loc[i,'Sample']
                lane = readFrame.loc[i,'Lane']
                if useSampleLane and pd.notnull(sample) and pd.notnull(lane): 
                    readset = sample + "_" + lane 
                else:
                    readset = 'ni{}'.format(c) ##ni = No Inventory
                readFrame.loc[i,'Read_Set'] = readset
                c += 1
    i = 0
    while sum(readFrame.duplicated(['Lab_ID','Read_Set'])) > 0: 
#         print('Read_Sett error')
#         print(sum(readFrame.duplicated(['Lab_ID','Read_Set'])))
        readFrame.loc[readFrame.duplicated(['Lab_ID','Read_Set']),'Read_Set'] = readFrame['Read_Set']+'r'+str(i)# pylint: disable=no-member
        i+=1                    
    

# def mergeReadDataFile(filename):
    
def listSAMFilesWithNames(directory,outfile=None,deep_search=True,sam_extension=sam_ext,verbose=False,bam_header=False):
    extSet = set(sam_extension)
    fileList = []
    fail = 0
    df = None
    ##Find all sam/bam files in this directory tree
    search_dir = os.path.abspath(directory)
    if deep_search:
        for rootdir, _, files in os.walk(search_dir):
            first_file = True
            for filename in files: ##TODO refactor
                if os.path.splitext(filename)[1] in extSet:
                    if first_file:
                        if verbose:
                            print("\t Collecting files from directory: "+rootdir)
                        first_file = False
                    fileList.append(os.path.join(rootdir,filename))
                else:
                    if verbose:
                        print("ignoring file: "+filename)
    else:
        all_files = os.listdir(search_dir)
        first_file = True
        for filename in all_files: ##TODO refactor
            if os.path.splitext(filename)[1] in extSet:
                if first_file:
                    print("\t Collecting files from directory: "+search_dir) 
                    first_file = False
                fileList.append(os.path.join(search_dir,filename))
            else:
                if verbose:
                    print("ignoring file: "+filename)        

    if len(fileList) > 0:
        genomeList = []
        for filename in fileList:
            sample_name = guessNameFromGenomeFile(filename) #default is ''
            if sample_name == '':
                fail += 1
                sample_name = 'MAP_{}'.format(fail)
            genomeList.append([sample_name,filename])
        if len(genomeList) > 0:
            df = pd.DataFrame(genomeList,columns = dfHeaders)
            df_trim = df[df['Lab_ID'] != '']
            if len(df_trim) > 0:
                g = df_trim.groupby('Lab_ID')
                unique = len(g)
                print("Found {} read mapping files in {}.\n Failed to identify names for {}.\n There were {} unique names".format(len(fileList),directory,fail,unique))
            else:
                print("Could not find any sample identifiers")
            df.sort_values('Lab_ID')
            ##TODO merge
            if outfile is not None:
                genomeFrame = None ##Append to exsiting directory file if it exists
                if os.path.isfile(outfile):
                    genomeFrame = pd.read_table(outfile) 
                    print("Appending genome list to existing file: "+outfile)
                    genomeFrame = pd.concat([genomeFrame,df],ignore_index=True)
                else:
                    genomeFrame = df
                    print("Saving list to "+outfile)
                genomeFrame.to_csv(outfile,sep='\t',index=False)
            
        else:
            print("Failed to identify files in directory {}".format(directory))
    else:
        print("Failed to identify files with the following extensions: "+','.join(sam_extension))
    if bam_header:
        df.rename(columns={'Filename':'BAM_File'},inplace=True)      
    return df
    
def openReadDataFile(filename):
    assert os.path.isfile(filename), "Read data file disappeared!"
    
    ##Header does not have standard position...
    maxHeader = 10
    i = 0
    needHeader = True
    result = None
    while needHeader and (i < maxHeader):
        try:
            DataFrame = pd.read_excel(filename,header=i)
        except:
            pass
        else:
            cols = DataFrame.columns
            needHeader = not (set(read_data_fileHeaders) <= set(cols))
        i += 1
        
    if needHeader:
        print("Failed to open read data file")
    else:
        result = DataFrame[read_data_fileHeaders].rename(columns={'Sample ID':'Sample'}) ##This should match PairReads table
        result['Lane'] = result['Lane'].map("L{:03d}".format)
    return result


##Returns None if no fastq to pair     
def pairReads(fileList,verbose=False,read_codes=None,useLabID=True):
    if read_codes is None:
        read_codes = df_read_codes    
    readFrame = None
    if len(fileList) <= 0:
        print('Error: no fastq files to pair')
    else: # >0
        fail = 0
        ##Sort files by sample identifier
        readLists = defaultdict(list)
        for filename in fileList:
            basename = os.path.basename(filename)
            isolate_name = guessNameFromGenomeFile(basename) if useLabID else '_'.join(basename.split('_')[:-4])
            if isolate_name == '':
                fail += 1
                isolate_name = '_'.join(basename.split('_')[:-4]) ##Cut off the last 4 sections of the illumina file format
                if isolate_name == '':
                    isolate_name = basename.split('.')[0] ##Take everything before the dot. This handles eddie's weird format 
                print("non-standard isolate name: {}".format(isolate_name))
            readLists[isolate_name].append(filename)
        if len(readLists) <= 0:
            print("Error: no isolates have reads")
        else: # >0
#             , "read list to be paired was empty or lacks BML sample identifier: "+'; '.join(fileList)
        ##Pair up paired-end reads and label with sample ID
            rows = []
            for sample,reads in readLists.items():
                if len(reads) == 1:
                    ##Deal with unpaired reads
                    readFile = reads[0]
                    read_info = dict()
                    read_info['Lab_ID'] = sample
                    read_info['Read1'] = readFile
                    rows.append(read_info)
                    if verbose:
                        print("Single read for {}".format(sample))
                elif len(reads) > 1: 
                    ##Pair them up; it is possible to get multiple read files from a single library on a single run
                    read_dir = defaultdict(list)
                    readInfo = dict()
                    for readFile in reads:       
                        readInfo[readFile] = parseIlluminaNames(readFile,read_codes=read_codes,verbose=verbose)
                        assert readFile in readInfo.keys(), "Unable to find description for file: {}".format(readFile)
                        read_info = readInfo[readFile]
                        if (read_info['Lab_ID'] == ''):
                            read_info['Lab_ID'] = sample 
                        read_direction = read_info['Read']
                        if read_direction is not None:
                            read_dir[read_direction].append(readFile)
                        else:
                            read_info = read_info.copy() ## modify it
                            ##Has no "Read"
                            read_info['Read1'] = readFile
                            rows.append(read_info)
                            print("Warning: Found multiple read files for {} but one has no read direction code {}".format(sample,readFile))
                    if (len(read_dir[read_codes[0]]) == len(read_dir[read_codes[1]])):
                        ##Pair them up
                        for read_code in read_dir.keys():
                            read_dir[read_code].sort()
    #                         if _verbose: print(read_dir.keys())
                        for (read1, read2) in itertools.zip_longest(read_dir[read_codes[0]],read_dir[read_codes[1]]):
                            assert read1 in readInfo.keys(), "Unable to find description for file: {}".format(read1)
                            read1_info = readInfo[read1].copy()
                            del read1_info['Read']
                            assert read2 in readInfo.keys(), "Unable to find description for file: {}".format(read2)
                            read2_info = readInfo[read2].copy()
                            del read2_info['Read']
                            if read1_info == read2_info:
                                ##use one of these as framework for data in row
                                read1_info['Read1'] = read1
                                read1_info['Read2'] = read2
                                rows.append(read1_info)
                            else:
                                print("Warning: cannot pair read files for {}".format(sample)) 
                                read1_info['Read1'] = read1
                                rows.append(read1_info)
                                read2_info['Read2'] = read2
                                rows.append(read2_info)
                    else:
                        print("Warning: Found multiple read files but was unable to pair them")
                        for read in read_dir[read_codes[0]] + read_dir[read_codes[1]]:
                            rows.append({'Lab_ID':sample,'Read1':read})        
    # Find some way to match up the unpaired read files 
    #                     del read_dir[r1]
    #                     del read_dir[r2]
    #                     for dir, reads in read_dir.items():
    #                         for read in reads:            
    #                             rows.append({'Lab_ID':sample,'Read1':read})  
                            
                else:
                    raise Exception("You can't have a sample with no reads!")
            #### Results here!!!
            readFrame = pd.DataFrame(rows)
            if fail > 0:
                print("Failed to identify the sample name for {} read files.".format(fail))
            ##Order the columns
            cols = readFrame.columns.tolist()
            coreCols = ['Lab_ID','Read1','Read2']
            newCols = [x for x in coreCols if x in cols] + [x for x in cols if x not in coreCols]
            readFrame = readFrame[newCols].copy()                
    return readFrame

def parseIlluminaNames(filename,read_codes=None,verbose=True):
    if read_codes is None:
        read_codes = df_read_codes     
    basename = os.path.basename(filename).rstrip(read_ext) #Not making this a variable
    ##Identify read code first. If they can be found as part of the full Illumina Regex, they will be over-written
    read_parse = None
    for r in read_codes:
        if r in  basename:
            read_parse = r
            break #Take R1 preferentially 
    IlluminaRegex1 = re.compile(r'(.*)_([GACT\-]*)(_(L\d{3}))?(_(R[12]))?(_(\d{3}))?(\..*)?$') #sample_barcode_lane_read_set.ext; this is for Hiseq and BCFB , not our MiSeq
    IlluminaRegex2 = re.compile(r'(.*)_(S\d+)(_(L\d{3}))?(_(R[12]))?(_(\d{3}))?(\..*)?$') #For our Miseq
    #     Illumina FASTQ files use the following naming scheme (5 items):
    # <sample name>_<barcode sequence>_L<lane (0-padded to 3 digits)>_R<read number>_<set number (0-padded to 3 digits>.fastq.gz
    IlluminaMatch1 = IlluminaRegex1.match(basename)
    IlluminaMatch2 = IlluminaRegex2.match(basename)
    if IlluminaMatch1:
        (sample,barcode,lane,read,illumina_set) = IlluminaMatch1.group(1,2,4,6,8)
        sample_number=None
    elif IlluminaMatch2:
        (sample,sample_number,lane,read,illumina_set) = IlluminaMatch2.group(1,2,4,6,8)
        barcode=None
    else:
#         splits = basename.split('_')[:-4]
        barcode = None
        lane = None #I could try to extract this
        sample_number=None
        illumina_set = None
        read = read_parse
        sample = basename.replace(read,'') if read is not None else basename #So that it is identical for paired reads
        if verbose:
            print("Unable to parse Illumina codes for {}".format(basename))
#             print(filename)
#             assert read in read_codes, "Unclear read direction {} code for {}".format(read,filename)
#             isolate_name = guessNameFromGenomeFile(sample)
#             if _verbose: print('File: {} \n Sample: {}'.format(filename,isolate_name))
    if read is None:
        read = read_parse 
    isolate_name = guessNameFromGenomeFile(filename) 
    return {'Lab_ID':isolate_name,
                          'Sample':sample,
                          'Barcode':barcode,
                          'Sample_Number':sample_number,
                          'Lane':lane,
                          'Read':read,
                          'Set':illumina_set
                          }
#             if _verbose: print(readInfo[filename])

###Input frames come from the "listAssembly" and "listSAM" routines, above
## Returns a merged frame if they can be reasonably matched -- otherwise returns None 
def mergeAssWithSam(assFrame,samFrame):
    try:
        if ('Filename' in samFrame.columns) and ('BAM_File' not in samFrame.columns):
            samFrame = samFrame.rename(columns={'Filename':'BAM_File'})      
        updateFrame = pd.merge(assFrame,samFrame,on='Lab_ID',how='outer')
    except RuntimeError:
        updateFrame = None
    return updateFrame
    
## Checks that the matching of assemblies to bam files makes sense.
### Most stringent is to require a one-to-one match of each assembly to each bam
### Less stringent criteria allow bams or assemblies to be subsets of each other -- but not allow unmatched instances of each
### Each BAM file must be matched to a unique assembly, but assemblies can used for to multiple BAMs if "uniqueBAM" is False
def validateAssSamMatch(mergedFrame,one2one=False, uniqueBAMs = True):
    result = True
    assemblySeries = mergedFrame.Filename
    assemblyRows = sum(assemblySeries.notnull())
    assemblyCount = len(assemblySeries.unique())
    bamSeries = mergedFrame.BAM_File
    bamRows = sum(bamSeries.notnull())
    bamCount = len(bamSeries.unique())
    bothRows = sum(bamSeries.notnull() & assemblySeries.notnull())
    ##1 to 1 relationship for all assemblies/bam
    if len(mergedFrame) == bamCount == assemblyCount: 
        print("Found unique SAM/BAM files for all {} assemblies".format(bamCount))    
    else:
        if one2one:
            print("Failed to match all assemblies to mapping files...")
            result = False
            ###Report on legit options                                
        if len(mergedFrame) == assemblyCount: ##No duplicate assemblies; fewer BAM files
            if bamCount == bamRows:##Each BAM had a unique assembly match
                print("Found unique SAM/BAM file for {} out of {} assemblies".format(bamCount,assemblyCount))  
    ###Bad conditions: cannot uniquely match stuff. These may be legit but need examination
    if bamCount != bamRows:
        result = False
        print("WARNING: BAM/SAM files could not be uniquely matched to assemblies ({} BAM for {} assemblies)".format(bamCount,bamRows))
    if (assemblyCount != assemblyRows):
        if uniqueBAMs: 
            result = False
        print("WARNING: Assembly files could not be uniquely matched to BAM ({} assemblies for {} BAMS)".format(assemblyCount,assemblyRows))   
    if (assemblyCount < len(mergedFrame)) and (bamCount < len(mergedFrame)):
        result = False
        print("WARNING: Both BAM and assembly files are unmatched -- confirm that they are matched properly and resubmit guide file")
    return result   

def matchAssToSam(assFrame,samFrame):
    updateFrame = mergeAssWithSam(assFrame,samFrame)
    valid_sams = validateAssSamMatch(updateFrame)
    return updateFrame if valid_sams else None 

# def placeAssembliesIntoDataFrame(argv,GO_settings=None,repository=None,rename_duplicateID=True,drop_duplicate_files=True):
#     return place_WGS_records_into_dataframe(argv,GO_settings,repository,rename_duplicateID,drop_duplicate_files,is_reads=False)
# 
# def placeReadsIntoDataFrame(argv,GO_settings=None,repository=None,rename_duplicateID=True,drop_duplicate_files=True):
#     return place_WGS_records_into_dataframe(argv,GO_settings,repository,rename_duplicateID,drop_duplicate_files,is_reads=True)
# 
# def place_WGS_records_into_dataframe(argv,GO_settings=None,repository=None,rename_duplicateID=True,drop_duplicate_files=True,is_reads=False):  
#     assert len(argv) > 1, "No arguments passed. Failure."
#     result = None
#     isolates = None
#     main_arg = argv[1]
#     if os.path.exists(main_arg): 
#         if len(argv) == 3: ## Main file and a genome name
#             if os.path.isfile(main_arg):
#                 genome_name = argv[2]
#                 result = pd.DataFrame({'Lab_ID':[genome_name],'Filename':[main_arg]})
#             else:
#                 print("usage: {} GenomeFile GenomeName".format(os.path.basename(argv[0])))
#                 print("\tNot a file: {}".format(argv[1]))
#                 print("\tFull path: {}".format(os.path.abspath(argv[1])))
#         elif len(argv) == 2: #a single argument pointing to a group of files
#             if os.path.isdir(main_arg): #assemble group list
#                 print('## Scanning genome directory ##')
#                 result = NGS_data_utilities.listReadFilesWithNames(main_arg) if is_reads else NGS_data_utilities.listGenomeFilesWithNames(main_arg)
#                 print("## Finished scanning directory ## \n")
#             elif os.path.isfile(main_arg): #read group list
#                 print("## Reading table ##")
#                 df = pd.read_table(main_arg)
#                 print("Table contains {} sequences to analyze".format(len(df)))
#                 if "Filename" in df.columns:
#                     print("\tUser provided assembly files")
#                     result = df
#                 else:
#                     file_type = 'read' if is_reads else 'assembly'
#                     print("\tPulling {} files from repository".format(file_type))
#                     isolates = df['Lab_ID'].tolist()
#         else:
#             print("Unable to interpret command line. Too many arguments")
#     else: #Finally, test if these are a list of isolates
#         print("The supplied argument is not a directory or file; assuming it is an isolate ID")
#         isolates = argv[1:]
#     if result is None and isolates is not None:
#         if repository is None:
#             settingDict = get_default_settings(GO_settings)
#             if settingDict is not None:
#                 repository = settingDict['repository']
#         if repository is not None and os.path.isdir(repository):
#             inventory = InventoryReader(repository)
#             if inventory.valid:
#                 if is_reads:
#                     print("Error: ability to select reads by isolate ID is not supported. Contact developer.")
#                     result = None
#                 else:
#                     gd,_ = inventory.getAssemblyRecords(isolates, ActiveOnly=True)
#                     result= gd[NGS_data_utilities.dfHeaders]
#             else:
#                 result = None
#         else:
#             print("Cannot find repository at {}:".format(repository))
#     if result is None or len(result)==0:
#         print("Unable to parse arguments")
#     else:
#         if drop_duplicate_files:
#             result = result.drop_duplicates() ##for those situations where the direcotry was indexed twice... no big deal
#         ##Make sure no two sequence files use the same genome name (this is used to identify intermediate files -- mainly matters for debugging
#         if rename_duplicateID:
#             result['Unique_ID'] = result['Lab_ID']
#             i = 0
#             while sum(result['Unique_ID'].duplicated()) > 0:
#                 result.loc[result['Unique_ID'].duplicated(),'Unique_ID'] = result['Unique_ID']+'r'+str(i)# pylint: disable=no-member
#                 i+=1
#     return result        

import argparse
import glob
      
def main():
    epi_text = ('If no NGS data directory is given, will automatically scan the following directories recursively: \n' +
                '\tread directory: {}'.format(default_read_dir) +
                '\n\tassembly directory: {}'.format(default_ass_dir)+
                '\n\tMiSeq directories: {}'.format(','.join(BML_read_locations)))

    parser = argparse.ArgumentParser(description='A program collect information about NGS data files',epilog=epi_text)
    ### general info
    parser.add_argument('--version','-V',action='version',version='%(prog)s {}.{}'.format(SCRIPT_VERSION,SCRIPT_SUBVERSION))
#     parser.add_argument('--debug',action='store_true',help="Preserve intermediate files and do not update reference files")

    ### controls

    ### required
    parser.add_argument('--assembly_dir','-ad',help='Directory with assemblies')
    parser.add_argument('--read_dir','-rd',help='Directory with reads')
    parser.add_argument('--out_dir','-od',help='Output directory')   
    parser.add_argument('--MiSeq_dir','-md',help='Directory with MiSeq reads and sample sheets')
    parser.add_argument('--misname_file','-mf',help='Excel spreadsheet with name corrections',default=default_misname_file,type=str)
#     parser.add_argument('')   
    args = parser.parse_args()
    out_dir = args.out_dir if args.out_dir else utilities.safeMakeOutputFolder(_outputBase)
    
    logFile = os.path.join(out_dir,default_logfile)
    print("LogFile is : "+logFile)
    sys.stdout = utilities.Logger(logFile)    
    print(_outputBase)
    
    ass_out = os.path.join(out_dir,assemblies_file)
    read_out = os.path.join(out_dir,reads_file)
    Mi_out = os.path.join(out_dir,MiSeq_files)
    mirror_out = os.path.join(out_dir,mirrored_reads)
    motif_out = os.path.join(out_dir,'Motif_Extra.txt')
#     NCBS_out = os.path.join(out_dir,NCBS_processed)
    if isinstance(args.misname_file,str):
        if os.path.exists(args.misname_file):
            pass
    if args.read_dir or args.assembly_dir or args.MiSeq_dir:
        if args.read_dir:
            listReadFilesWithNames(args.read_dir,outfile = read_out,read_extension=read_ext,verbose=False,doAssignReadSets=True)
        if args.assembly_dir:
            listGenomeFilesWithNames(args.assembly_dir,outfile = ass_out, deep_search = True, verbose = False)
        if args.MiSeq_dir:
            listReadsFromMiSeqToplevel(args.MiSeq_dir, outfile=Mi_out, read_extension=read_ext, verbose=False, doAssignReadSets=False)
    else:
        print("\nStarting BML MiSeq reads...")
        df = listReadsFromMiSeqToplevel(BML_read_locations, outfile=Mi_out, read_extension=read_ext, verbose=True, doAssignReadSets=False)
        print("\tReported {} records".format(len(df)))
        print("Starting BCFB reads...")
        df = listReadFilesWithNames(default_read_dir,outfile = read_out,read_extension=read_ext,verbose=False,doAssignReadSets=True)
        print("\tReported {} records".format(len(df))) 
        ##Assemblies and associated files       
        print("\nStarting BCFB assemblies...")
        df = listGenomeFilesWithNames(default_ass_dir,outfile = ass_out, deep_search = True, verbose = False)
        print("\tReported {} records".format(len(df)))
        motif_base = df.Filename.str.rstrip('.fasta')
        for i in motif_base.index:
            f = motif_base[i]
            matches = glob.glob(f+"*"+motif_ext)
            if len(matches) > 1:
                print("Warning, found multiple motif files for {}. Selecting first one by glob.".format(f))
            elif len(matches) == 1:
                motif_base[i] = matches[0]
#         motif_files = df.Filename.str.rstrip('.fasta') + motif_ext
        motif_exists = motif_base.apply(os.path.isfile)
        print("\tIdentified {} associated motif files".format(sum(motif_exists)))
        if sum(motif_exists) > 0:
            df.loc[motif_exists,'Motif_Data'] = motif_base.loc[motif_exists]
        basepath = df.Filename.str.extract(r'(^.*\/[^.]*\.[^.]*)[^/]')#,expand=False)
        summary_files = basepath + '.summary'
        summary_exists = summary_files.apply(os.path.isfile)
        if sum(summary_exists) >0:
            df.loc[summary_exists,'BLAST_summary'] = summary_files.loc[summary_exists]
        circlator_files = basepath + '.circlator.json'      
        circlator_exists = circlator_files.apply(os.path.isfile)      
        if sum(circlator_exists) >0:
            df.loc[circlator_exists,'Circulator'] = circlator_files.loc[circlator_exists]            
        df.to_csv(ass_out,sep='\t',index=False) ## ovirwrite file from listGenomesFileWithNames
        ##Get all motif for comparison
        motif_list = []
        for rootdir, _, files in os.walk(default_ass_dir):
            motif_list += [os.path.join(rootdir,x) for x in files if x.endswith(motif_ext)] 
        extra_motif = [x for x in motif_list if x not in df.Motif_Data.tolist()]
        if len(extra_motif) > 0:
            print("Found extra motif files. Saving list to {}".format(motif_out))
            with open(motif_out,'wt') as fout:
                for f in extra_motif:                   
                    print(f,file=fout)
        
        ##Get the NCBS stuff
        print("Starting BCFB mirrored reads...") ##Note, this contains some files that were deleted from our main data directory
        NCBS_raw = listReadFilesWithNames(default_read_mirror,outfile = mirror_out,read_extension=read_ext,verbose=False,doAssignReadSets=True)
        print("\tReported {} mirrored reads".format(len(NCBS_raw)))
                 
#         print("Starting NCBS trimmed reads...")
#         NCBS_trimmed = listReadFilesWithNames(default_NCBS_dir,outfile = None ,read_extension='trim.fq.gz',verbose=False,doAssignReadSets=False)
#         print("\tReported {} mirrored reads".format(len(NCBS_trimmed)))        
#         print("\nStarting NCBS assemblies...")
#         NCBS_assembly = listGenomeFilesWithNames(default_NCBS_dir,outfile = None , deep_search = True, verbose = False,extension = 'contigs.fasta')
#         print("\tReported {} records".format(len(NCBS_assembly)))
#         NCBS_assembly_raw = NCBS_assembly[NCBS_assembly.Filename.str.contains("Alignment_Results")]
#         print("\t {} raw assemblies".format(len(NCBS_assembly_raw)))
#         NCBS_assembly_clean = NCBS_assembly[NCBS_assembly.Filename.str.contains("Assembly_Cleanup")]
#         print("\t {} clean assemblies".format(len(NCBS_assembly_clean)))
#         NCBS_assembly_discard = listGenomeFilesWithNames(default_NCBS_dir,outfile = None , deep_search = True, verbose = False,extension = 'contigs_discarded.fasta')
#         print("\t {} discarded assemblies".format(len(NCBS_assembly_discard)))
#         NCBS_reads = pd.merge(NCBS_raw,NCBS_trimmed,suffixes=('raw','trimmed'))
#         NCBS_assemblies = pd.merge(NCBS_assembly_raw,NCBS_assembly_clean,suffixes=('','cleaned'))
#         NCBS_assemblies = pd.merge(NCBS_assemblies,NCBS_assembly_discard,suffixes=('raw','discarded'))
#         NCBS_total = pd.merge(NCBS_reads,NCBS_assemblies)
#         NCBS_total.to_csv(NCBS_out,index=False,sep='\t')
                              

#         data_extra = '/sc'

        
        

    
    
if __name__ == "__main__":
    if not utilities.has_preferred_python():
        raise Exception("Upgrade your python version")
    main()

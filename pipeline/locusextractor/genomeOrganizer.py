#! /bin/env python3

### This module is designed to identify the genomic data files in our laboratory's data directories
##by Adam Retchless
## April 7, 2015, script_version 0.6
script_version = 0.13
script_subversion = 22
##Note: Need to test the ability to link read files to the assembly, or inventory them independently

#pylint: disable=global-statement, broad-except
import re
import os
import pandas as pd
from Bio import SeqIO
import sys
import gzip
import zlib
import stat
import time
from shutil import copyfile
from collections import defaultdict
import functools
import urllib.request 
import utilities
import seq_utilities
import NGS_data_utilities
# import seq_utilities

_verbose = False  ##Set to True by Debug

Repository = '' #This must be set either by the user or from the settings file
ASSEMBLY_DIR_REPO = 'assemblies'
READ_DIR_REPO = 'reads'
INVENTORY_FILE_BASE = 'inventory.tab'
READMAP_FILE = 'read_assembly_map.tab'

read_ext = '.fastq.gz'
# read454_Ext = '.sff'

my_file = __file__
if os.path.islink(my_file):
    my_file = os.path.realpath(my_file)
SCRIPT_DIR, SCRIPT_NAME = os.path.split(my_file)
SCRIPT_DIR = os.path.abspath(SCRIPT_DIR)

############################
#### Functions for organizing files (e.g. interpreting names)
#########################
def getBaseID(sample_name,version):
    return "{}_v{}".format(sample_name,version)
    
# Helper functions to improve the CLI for outside scripts
def default_list(destination_directory):
    if os.path.isdir(destination_directory):
        result = os.path.join(destination_directory,'genome_list.tab')
    else:
        result = None
    return result

def placeAssembliesIntoDataFrame(argv,GO_settings=None,repository=None,rename_duplicateID=True,drop_duplicate_files=True,deep_search=True):
    return place_WGS_records_into_dataframe(argv,GO_settings,repository,rename_duplicateID,drop_duplicate_files,is_reads=False,deep_search=deep_search)

def placeReadsIntoDataFrame(argv,GO_settings=None,repository=None,rename_duplicateID=True,drop_duplicate_files=True):
    return place_WGS_records_into_dataframe(argv,GO_settings,repository,rename_duplicateID,drop_duplicate_files,is_reads=True)

def place_WGS_records_into_dataframe(argv,GO_settings=None,repository=None,rename_duplicateID=True,drop_duplicate_files=True,is_reads=False,deep_search=True):  
    assert len(argv) > 1, "No arguments passed. Failure."
    result = None
    isolates = None
    main_arg = argv[1]
    if os.path.exists(main_arg): 
        if len(argv) == 3: ## Main file and a genome name
            if os.path.isfile(main_arg):
                genome_name = argv[2]
                result = pd.DataFrame({'Lab_ID':[genome_name],'Filename':[main_arg]})
            else:
                print("usage: {} GenomeFile GenomeName".format(os.path.basename(argv[0])))
                print("\tNot a file: {}".format(argv[1]))
                print("\tFull path: {}".format(os.path.abspath(argv[1])))
        elif len(argv) == 2: #a single argument pointing to a group of files
            if os.path.isdir(main_arg): #assemble group list
                print('## Scanning genome directory ##')
                result = NGS_data_utilities.listReadFilesWithNames(main_arg) if is_reads else NGS_data_utilities.listGenomeFilesWithNames(main_arg,deep_search=deep_search)
                print("## Finished scanning directory ## \n")
            elif os.path.isfile(main_arg): #read group list
                print("## Reading table ##")
                df = pd.read_table(main_arg)
                print("Table contains {} sequences to analyze".format(len(df)))
                if "Filename" in df.columns:
                    print("\tUser provided assembly files")
                    result = df.copy()
                elif "Lab_ID" in df.columns:
                    file_type = 'read' if is_reads else 'assembly'
                    print("\tCould not identify 'Filename' field. Pulling {} files from repository".format(file_type))
                    isolates = df['Lab_ID'].tolist()
                else:
                    print("Cannot parse file. Please provide a tab-delimited table with headers 'Filename' and 'Lab_ID'")
                    ##Leaves result as none
        else:
            print("Unable to interpret command line. Too many arguments")
    else: #Finally, test if these are a list of isolates
        print("The supplied argument is not a directory or file; assuming it is an isolate ID")
        isolates = argv[1:]
    if result is None and isolates is not None:
        if repository is None:
            settingDict = get_default_settings(GO_settings)
            if settingDict is not None:
                repository = settingDict['repository']
        if repository is not None and os.path.isdir(repository):
            inventory = InventoryReader(repository)
            if inventory.valid:
                if is_reads:
                    print("Error: ability to select reads by isolate ID is not supported. Contact developer.")
                    result = None
                else:
                    gd,_ = inventory.getAssemblyRecords(isolates, ActiveOnly=True)
                    result= gd[NGS_data_utilities.dfHeaders]
            else:
                result = None
        else:
            print("Cannot find repository at {}:".format(repository))
    if result is None or len(result)==0:
        print("Unable to parse arguments")
    else:
        if drop_duplicate_files:
            result = result.drop_duplicates() ##for those situations where the direcotry was indexed twice... no big deal
        ##Make sure no two sequence files use the same genome name (this is used to identify intermediate files -- mainly matters for debugging
        if rename_duplicateID:
            NGS_data_utilities.assignUniqueID(result)
    return result


###########################
#### Functions for manipulating the inventory files
###########################

def forcedIntCasting(my_series):
    return my_series.str.split('.').str.get(0).astype(int)   
    ##alt strategy is to first cast to float
    ##Allow exceptions to rise to the next level... though maybe I could return None to indicate failure
 
##Test that each isolates has one and only one record
def recordsAreCompleteAndUnique(Records,isolates):
    valid = True
    for i in isolates:
        valid = sum(Records['Lab_ID'] == i) == 1
        if not valid:
            break
    return valid
    
##Active only should only be selected when reading only    
def assemblySetup(assembly_file,relative_path=None,ValidOnly=False): ##TODO: the udpate file does not necessarily have all the fields of the assembly frame .. which causes problem
    try:
        assembly_frame = pd.DataFrame(pd.read_table(assembly_file,dtype=str),copy=True) ##If we're not careful, it will interpret ints as floats and cause bugs
        assembly_frame.dropna(how='all',inplace=True)
        for c in inventoryHeaders:
            if c not in assembly_frame.columns:
                assembly_frame[c] = None ##None causes problems with type-casting, below
    except IOError:
        assembly_frame = pd.DataFrame(columns=inventoryHeaders)
    if len(assembly_frame) > 0: ##Make filepaths absolute : all assembly files are in the repository
        if relative_path is not None:
            inventory_path_join = functools.partial(DeRelativizePath,relative_path)
            for c in assFileKeys:
                if c in assembly_frame.columns:
                    good_values = assembly_frame[c].notnull()
                    assembly_frame.loc[good_values,c] = assembly_frame[good_values][c].apply(inventory_path_join)
    #Set index
    assembly_frame['Version'] = assembly_frame['Version'].astype(int)
    assembly_frame.set_index(['Lab_ID','Version'],drop=False,inplace=True)
    #Make temporary changes that affect empty cells; use "valid" to revert them
    frame_valid = assembly_frame.notnull()
    assembly_frame['Invalid'] = assembly_frame['Invalid'].isin(['True','TRUE','1','1.0','yes','Yes','YES'])
    assembly_frame['Active'] = (~assembly_frame['Active'].isin(['False','FALSE','0','0.0','no','No','NO'])) & (assembly_frame['Invalid'] != True)
    if ValidOnly:
        assembly_frame = assembly_frame[assembly_frame['Invalid'] != True]       
    assembly_frame['Gaps'] = ~assembly_frame['Gaps'].isin(['False','FALSE','No','NO','no','0'])  
    ##Cast everything to the appropriate datatype
    castAssemblyColumns(assembly_frame)
    return assembly_frame, frame_valid 

##Address this bug: https://github.com/pydata/pandas/issues/4094
def castAssemblyColumns(assembly_frame):
    for _,row in inventoryHeadersFrame.iterrows():
        field = row["Field"]
        field_type = row['dtype']
        if field in assembly_frame.columns:
            try:
                assembly_frame[field] = assembly_frame[field].astype(field_type)
            except (ValueError,TypeError):
                no_good = True
                if field_type is int:
                    try:
                        assembly_frame[field] = forcedIntCasting(assembly_frame[field])
                    except:
                        no_good = True
                    else:
                        no_good =False
                        print("Forced floating points to ints for {}".format(field))                    
                if no_good:    
                    print("Failed to cast {} to {}".format(field,field_type))    
    
##Active only should only be selected when reading only
def readSetup(read_file,relative_path=None,ValidOnly=False):
    try:
        read_frame = pd.DataFrame(pd.read_table(read_file,dtype=str),copy=True)
        read_frame.dropna(how='all', inplace=True)
        for c in readInventoryHeaders:
            if c not in read_frame.columns:
                read_frame[c] = None
    except IOError:
        read_frame = pd.DataFrame(columns=readInventoryHeaders)
    if len(read_frame) > 0: #Make filepaths absolute: reads must be in GWA or have HTTP
        if relative_path is not None:
            read_path_join = functools.partial(DeRelativizePath,relative_path)
            rf = read_frame
            for c in readFileKeys + ['Original_Read1','Original_Read2']:
                relative_reads = utilities.avoidItemsThatStartWith(rf,c,'http:') ##Anything that is not HTTP is relative
                rf.loc[relative_reads,c] = rf[relative_reads][c].apply(read_path_join)    
    #Set index
    try:
        read_frame['Read_Set'] = read_frame['Read_Set'].astype(int)
    except:
        try:
            read_frame['Read_Set'] = forcedIntCasting(read_frame['Read_Set'])
        except ValueError:
            print("Failed to cast {} to {}".format('Read_Set',int))
            
    read_frame.set_index(['Lab_ID','Read_Set'],drop=False,inplace=True) 
    #Make temporary changes that affect empty cells; use "valid" to revert them
    frame_valid = read_frame.notnull()
    read_frame['Invalid'] = read_frame['Invalid'].isin(['True','TRUE','1']) 
    if ValidOnly:
        read_frame = read_frame[read_frame['Invalid'] != True]   
  
    return read_frame, frame_valid
    
def readAssemblyMapSetup(readmap_file):
    readmap_frame = pd.read_table(readmap_file,dtype=str) if os.path.isfile(readmap_file) else pd.DataFrame(columns=readAssemblyMapHeaders)    
    ##Cast everything to the appropriate datatype
    for _,row in readAssemblyMapFrame.iterrows():
        field = row["Field"]
        field_type = row['dtype']
        try:
            readmap_frame[field] = readmap_frame[field].astype(field_type)
        except ValueError:
            no_good = True
            if field_type is int:
                try:
                    readmap_frame[field] = forcedIntCasting(readmap_frame[field])
                except:
                    no_good = True
                else:
                    no_good =False
                    print("Forced floating points to ints for {}".format(field))                    
            if no_good:    
                print("Failed to cast {} to {}".format(field,field_type))   
    return readmap_frame
        
def DeRelativizePath(start,path):
    if path[0] != '/':
        result = os.path.normpath(os.path.join(start,path))
    else:
        result = path
    return result
    
def conditionalRelativePath(start,path):
    if path[0] != '/':
        raise ValueError("Must work with absolute path, not {}".format(path))
    shared = os.path.commonprefix([start,path])
    if len(shared) > 1: #Not just '/
        result = os.path.relpath(path,start)
    else:
        result = path #No shared path,  so no value in making it relative
    return result
        
def assemblyPackup(assembly_frame,relative_path):
    af = assembly_frame.copy()
#     ass_rel_path = functools.partial(conditionalRelativePath,start=relative_path)
#     is_str = functools.partial(isinstance,classinfo=str)
    for c in assFileKeys:
        if c in af.columns:
            good_values = (af[c].notnull()) & (af[c] != '')  & (af[c] != 'nan')
            for g in good_values.index:
                if good_values[g]:
                    try:
                        af.loc[g,c] = conditionalRelativePath(relative_path,af.loc[g,c])
                    except ValueError as e:
                        print("Error on {}, index {}".format(c,g))
                        print(e)
                        raise
    return af 
    
def readPackup(read_frame,relative_path): 
    rf = read_frame.copy()
#     reads_rel_path = functools.partial(conditionalRelativePath,start=relative_path) 
    for c in readFileKeys:
        relative_reads = utilities.avoidItemsThatStartWith(rf,c,'http:') ##Anything that is not HTTP is made relative
        for r in relative_reads.index:
            if relative_reads[r]:
                rf.loc[r,c] = conditionalRelativePath(relative_path,rf.loc[r,c])
#                 temp = rf[relative_reads][c]
#         rf.loc[relative_reads,c] = temp.apply(reads_rel_path)
    return rf     
    
    
############ Class Based Inventory Manager #######################
##This is basically a wrapper for a set of dataframes representing the inventory files that controls a subdirectories in a repository

class Inventory:
    #Why arent' these just global constants?
    ASSEMBLY_DIR_REPO = 'assemblies'
    READ_DIR_REPO = 'reads'
    BAM_DIR_REPO = 'BAM'
    INVENTORY_FILE_BASE = 'inventory.tab'
    READMAP_FILE = 'read_assembly_map.tab'
    
    def __init__(self,repository=None):
        self.assembly_frame = self.read_frame = self.contig_frame = self.readmap_frame = None
        self.assembly_valid = self.read_valid = None
        if repository is None:
            repository = get_default_settings(SETTING_PATH)['repository']
        self.setRepository(repository)
        self.valid = False ##Needs to activate repository by initiating reader or writer
        self.readInvTemplate = pd.DataFrame(columns = readInventoryHeaders)
    
    def setRepository(self,repository):
                ##Set paths
        self.repository = os.path.abspath(repository)            
        self.assembly_directory = os.path.join(self.repository,self.ASSEMBLY_DIR_REPO)            
        self.read_directory = os.path.join(self.repository,self.READ_DIR_REPO)
        self.assembly_file = os.path.join(self.assembly_directory,self.INVENTORY_FILE_BASE)
        self.contig_file = utilities.appendToFilename(self.assembly_file,'_contigs')
        self.read_file = os.path.join(self.read_directory,self.INVENTORY_FILE_BASE)
        self.readmap_file = os.path.join(self.assembly_directory,self.READMAP_FILE)
        self.BAM_directory = os.path.join(self.repository,self.BAM_DIR_REPO)
        

    def repositoryExists(self):
        result = True
        result &= os.path.isdir(self.repository)
        result &= os.path.isdir(self.assembly_directory)
        result &= os.path.isdir(self.read_directory)
        return result
        
    def activateRepository(self,ValidOnly,r_verbose=True): #pylint: disable=attribute-defined-outside-init
        result = False
        if self.repositoryExists():
            try:
                if r_verbose or _verbose:
                    print("Activating repository at "+self.repository)
                ### Load the frames 
                self.assembly_frame, self.assembly_valid = assemblySetup(self.assembly_file,self.assembly_directory,ValidOnly=ValidOnly)
                vprint('Found {} valid assemblies and {} invalid'.format(sum(~self.assembly_frame.Invalid),sum(self.assembly_frame.Invalid)))
                    ## REad frame
                self.read_frame, self.read_valid = readSetup(self.read_file,self.read_directory,ValidOnly=ValidOnly)
                vprint('Found {} valid read sets and {} invalid'.format(sum(~self.read_frame.Invalid),sum(self.read_frame.Invalid)))
                    ##Other frames
                self.contig_frame = pd.read_table(self.contig_file,dtype=str) if os.path.isfile(self.contig_file) else pd.DataFrame(columns=inventoryContigHeaders)
                self.contig_frame['Version'] = self.contig_frame['Version'].astype(float).astype(int) ##This keeps getting saved as a floats (0.0) and can't be directly cast to int
                self.readmap_frame = readAssemblyMapSetup(self.readmap_file) 
                result = True
            except:
                print("Error reading repository files")
                raise
        if not result:
            print("ERROR: Unable to activate repository at "+self.repository)
            print("")
        return result
    
    ##Splits input frame into two parts: one for import (new), and one for lookup (existing)
    def compareWithExistingReads(self,inputFrame):
        ##First, split the input frame into old and new
        inputFrame = inputFrame.append(self.readInvTemplate) ##New object. Original input frame is unmodified.
        read1Bool = inputFrame.Read1.isin(self.read_frame.Original_Read1)
        read2Bool = inputFrame.Read2.isin(self.read_frame.Original_Read2)
        assert (read1Bool == read2Bool).all(), "Existing read files are matched with new files. Cannot proceed"                                                      
        readsExistingBool =  (read1Bool & read2Bool)
        readsExisting = inputFrame[readsExistingBool].copy()
        readsNew = inputFrame[~readsExistingBool].copy()
        ##Now find the matching reads already in the database
        Eread1Bool = self.read_frame.Original_Read1.isin(inputFrame.Read1)
        Eread2Bool = self.read_frame.Original_Read2.isin(inputFrame.Read2)
        assert (Eread1Bool == Eread2Bool).all(), "Existing read files are matched with new files (2). Cannot proceed"
        EreadsExsitingBool = (Eread1Bool & Eread2Bool)
        readsExistingInDB = self.read_frame[EreadsExsitingBool].copy()   
        ## Transfer the ReadSet identifier to the input frame to set index and copy files
        for i, row in readsExisting.iterrows():
            match = (readsExistingInDB.Original_Read1 == row['Read1']) & (readsExistingInDB.Original_Read2 == row['Read2'])
            read_set_list = readsExistingInDB[match]['Read_Set'].unique().tolist()
            if len(read_set_list) == 1:
                rs = read_set_list[0]
                readsExisting.loc[i,'Read_Set'] = rs
            else:
                ##TODO: this has not been tested
                print("Waring:")
                print("\tDuplicate entries for {}. Matching to version with most links".format(row.Lab_ID))
                try:
                    self.countReadLinks(False) ##recalculate all
                    idx = readsExistingInDB[match].idxmax('Link_Count')
                    readsExisting.loc[i,'Read_Set'] = readsExistingInDB.loc[idx,'Read_Set']
                except:
                    raise RuntimeError("Duplicate entries for {}. Cannot match to existing reads".format(row.Lab_ID))
        return readsExisting, readsNew

    ##TODO: Not tested 
    ###If this is going to be saved, the read_valid frame needs to be modified
    def countReadLinks(self,NaOnly=True):
        lc = 'Link_Count'
        if lc not in self.read_frame.columns:
            self.read_frame[lc] = None
        update_rows = self.read_frame[lc].isnull() 
        if not NaOnly: ## everything
            update_rows |= self.read_frame[lc].notnull() 
        for i, r in self.read_frame[update_rows].iterrows():
            link_count = int(sum((self.readmap_frame.Lab_ID == r['Lab_ID']) & (self.readmap_frame.Read_Set == r['Read_Set'])))
            self.read_frame.loc[i,'Link_Count'] = link_count   
            
    ###Warning: this will relead the inventory. Save first!           
    def linkInvalidAssToReads(self):   
        self.valid = self.activateRepository(ValidOnly=False,r_verbose=False) ##Reload for writing
        invalidAss = self.assembly_frame[self.assembly_frame.Invalid]
        linkBool = (self.readmap_frame.Lab_ID.isin(invalidAss.Lab_ID) & self.readmap_frame.Assembly_Version.isin(invalidAss.Version))
        invalidLinks = self.readmap_frame[linkBool]
        readBool = self.read_frame.Read_Set.isin(invalidLinks.Read_Set) & self.read_frame.Lab_ID.isin(invalidLinks.Lab_ID)
        questionableReads = self.read_frame[readBool].copy()
        self.valid = self.activateRepository(ValidOnly=True,r_verbose=False) ##Reload for writing  
        return questionableReads
        
        
class InventoryReader(Inventory):

    def __init__(self,repository=None):
        super().__init__(repository)
        self.valid = self.activateRepository(ValidOnly=True)
        
    def duplicateInventoryFiles(self,directory):
        print("Writing duplicate inventory files in "+directory)
        self.valid = self.activateRepository(ValidOnly=False,r_verbose=False) ##Reload for writing
        ##Retain absolute paths rather than making them relative
        utilities.safeMakeDir(directory)
        if len(self.assembly_frame) > 0:    
            dest= os.path.join(directory,'assembly_inventory.tab')
            try:
                assemblyPackup(self.assembly_frame.where(self.assembly_valid),directory).to_csv(dest,sep='\t',index=False)
            except IOError:
                print("ERROR: Unable to write to {}".format(dest))
        if len(self.contig_frame) > 0:
            dest = os.path.join(directory,'contig_inventory.tab')
            try:
                self.contig_frame.to_csv(dest,sep='\t',index=False)
            except IOError:
                print("ERROR: Unable to write to {}".format(dest))      
        if len(self.read_frame) > 0:
            dest = os.path.join(directory,'read_inventory.tab')
            try:
                readPackup(self.read_frame.where(self.read_valid),directory).to_csv(dest,sep='\t',index=False)
            except IOError:
                print("ERROR: Unable to write to {}".format(dest))                
        if len(self.readmap_frame) > 0:
            dest = os.path.join(directory,'reads_to_assemblies.tab')
            try:
                self.readmap_frame.to_csv(dest,sep='\t',index=False)
            except IOError:
                print("ERROR: Unable to write to {}".format(dest))   
        self.valid = self.activateRepository(ValidOnly=True,r_verbose=False)      

        
    def getAssemblyRecords(self,isolates,ActiveOnly = True):
        assert isinstance(isolates,list)
        ##Select assemblies
        af = self.assembly_frame
        allowedVersions = af['Active'] != False if ActiveOnly else af['Invalid'] != True
        activeFrame = af[af['Lab_ID'].isin(isolates) & allowedVersions].copy()
        ##Check that we got everything
        invList = activeFrame['Lab_ID'].tolist()
        invSet = set(invList)
        if len(invSet) < len(invList):
            print("Notice: Duplicate Active assemblies in inventory. Exporting all.")
        reqSet = set(isolates)
        if len(reqSet) != len(isolates):
            print('Notice: Duplicate values in isolate request list')
        assert reqSet.issuperset(invSet)
        if reqSet != invSet: 
            print("Notice: Not all genomes are present in our assembly Repository")
            ##Report if any are present as reads only
            missingSet = reqSet.difference(invSet)
            rf = self.read_frame
            readsOnly = rf[rf['Lab_ID'].isin(missingSet)]
            if len(readsOnly) > 0:
                print ("The following isolates are present in the read collection: {}".format(",".join(readsOnly['Lab_ID'].unique())))
        ### Get information about the contigs
        cf = self.contig_frame.set_index(['Lab_ID','Version'],drop=False)
        activeContigs = cf[cf['Lab_ID'].isin(activeFrame['Lab_ID'])]
        return activeFrame, activeContigs
    
    def exportAssemblies(self,isolates,destination,ActiveOnly=True,InventoryOnly=False, include_qual= False, include_tech=True):
        assert isinstance(isolates,list)
        if self.repository in destination:
            print("Cannot write to repository using this method. This is serious, so we're stopping everything")
            sys.exit(1)
        print("Exporting assemblies: {}".format(",".join(isolates)))
        utilities.safeMakeDir(destination)
        af,cf = self.getAssemblyRecords(isolates,ActiveOnly)
        contig_file = os.path.join(destination,os.path.basename(self.contig_file))
        assembly_file = os.path.join(destination,os.path.basename(self.assembly_file))
        utilities.safeOverwriteTable(contig_file, cf, 'tab',index=False)       
        if not InventoryOnly:
            af.rename(columns={'Filename':'Repository_File'},inplace=True)
            for idx, row in af.iterrows():
                baseID = getBaseID(idx[0],idx[1]) #Lab_ID and Version
                if include_tech:
                    tech = row['Technology'] if pd.notnull(row['Technology']) else "TechUnavail"
                    baseID += '_' + tech
                dest_filename = os.path.abspath(os.path.join(destination,baseID) + '.fasta')
                exportGenomeFASTA(row['Repository_File'],dest_filename,include_qual = include_qual)
                af.loc[idx,'Filename'] = dest_filename
        af['File_Basename'] = af.Filename.apply(os.path.basename)
        utilities.safeOverwriteTable(assembly_file,af,'tab',index=False)    
        return af
        
    
    def exportReads(self,isolates,destination,linked=True,InventoryOnly=False):
        assert isinstance(isolates,list)
        if self.repository in destination:
            print("Cannot write to repository using this method. This is serious, so we're stopping everything")
            sys.exit(1)
        print("Exporting reads: {}".format(",".join(isolates)))
        utilities.safeMakeDir(destination)      
        rf = self.read_frame
        new_frame = rf[rf.Lab_ID.isin(isolates)] 
        exportReadFrame(new_frame,destination,linked=linked,InventoryOnly=InventoryOnly)     
            
                     
                
    def getReadsWithoutAssembly(self,isolate_level = True):
        result = None
        if isolate_level:
            assembly_list = self.assembly_frame['Lab_ID'].unique().tolist()
            rf = self.read_frame
            result = rf[~rf['Lab_ID'].isin(assembly_list)]
        else: ##Use the read-assembly linkage
            print("Not implemented")
        return result
        
class InventoryWriter(Inventory):

    def __init__(self,repository=None):
        super().__init__(repository)
        self.createRepositoryPaths()
        self.valid = self.activateRepository(ValidOnly=False)

    def createRepositoryPaths(self):
        utilities.safeMakeDir(self.repository)
        utilities.safeMakeDir(self.assembly_directory)
        utilities.safeMakeDir(self.read_directory)
    
    ###UPdate file is a hand-modified file; this is to assure that I don't accidentally delete data    
    def update_assemblies(self,update_file):
        df,df_valid = assemblySetup(update_file,ValidOnly=False) ##Sets the index
        df = df.where(df_valid) ##So that we don't overwrite the filled-in boolean values
        ### Remove fields that we do not want to update
        update_columns = [x for x in df.columns if x not in inventoryHeadersStatic] 
        df = df[update_columns].copy() ##Index has already been set
        ##Update and reset the "valid" mask. Must first masked the current auto-fill values (Active, Invalid).
        af = self.assembly_frame.where(self.assembly_valid) ##So that we can track which fields have been filled in
        af.update(df) 
#         castAssemblyColumns(af)  ##previous step changes everything to float for some stupid reason (both af and df treat it as int)
        self.assembly_valid = af.notnull()
        ##Test if there has been updating
        same = (af.where(self.assembly_valid) == self.assembly_frame.where(self.assembly_valid))
        updated = not all(same.apply(all))
        if updated:
            self.assembly_frame.update(af) ##Keep the auto-filled values from assembly setup
            castAssemblyColumns(self.assembly_frame) ##Updating on subset changes everything to float. Can only cast back if default values are filled (no null)
        else:
            print("Unable to update assembly inventory with "+update_file)
        return updated

    ###UPdate file is a hand-modified file; this is to assure that I don't accidentally corrupt the data in an obvious way and there is a backup copy            
    def update_reads_fromFile(self,update_file):
        df,df_valid = readSetup(update_file,ValidOnly=False)
        df = df.where(df_valid)
        rf = self.read_frame.where(self.read_valid)
        rf.update(df)
        self.read_valid = rf.notnull()
        same = (rf.where(self.read_valid) == self.read_frame.where(self.read_valid))
        updated = not all(same.apply(all))
        self.read_frame.update(rf)
        if not updated:
            print("Unable to update read inventory with "+update_file)
        return updated        
        
        
    def saveInventoryFiles(self):
        ##Note: indicies are not dropped from the regular fields, so they should not be saved
        if len(self.assembly_frame) > 0:    
            temp_ass = assemblyPackup(self.assembly_frame.where(self.assembly_valid),self.assembly_directory)
            utilities.safeOverwriteTable(self.assembly_file, temp_ass, 'tab',index=False)
        if len(self.contig_frame) > 0:
            utilities.safeOverwriteTable(self.contig_file, self.contig_frame,'tab',index=False)      
        if len(self.read_frame) > 0:
            rf = readPackup(self.read_frame.where(self.read_valid),self.read_directory)
            utilities.safeOverwriteTable(self.read_file,rf,'tab',index=False)
        if len(self.readmap_frame) > 0:
            utilities.safeOverwriteTable(self.readmap_file,self.readmap_frame,'tab',index=False) 

    ###newFrame has new reads to incorporate into the inventory.
    ### existingUpdate has reads that already exist, but may have some additional data to incorporate (must be a free-form field; not one that gets default values added -- e.g. Invalid)        
    def mergeReadsWithInventory(self,newFrame,existingUpdate):
        readsAdded = pd.DataFrame()
        for _, row in newFrame.iterrows():
            read_set_frame = self.read_frame[self.read_frame['Lab_ID'] == row['Lab_ID']]
            candidate_set =  len(read_set_frame)
            while candidate_set in read_set_frame.Lab_ID:
                candidate_set += 1
                assert candidate_set < 2 * len(read_set_frame) + 1, "Unable to calculate a new read sets id for {}. Something is wrong. Aborting ".format(row['Lab_ID'])
            row.loc['Read_Set'] = candidate_set
            self.read_frame = self.read_frame.append(row,ignore_index=True)
            readsAdded = readsAdded.append(row,ignore_index=True)
        if len(existingUpdate) > 0:
            self.read_frame.update(existingUpdate.set_index(['Lab_ID','Read_Set'],drop=False) ,overwrite=False) ##Be conservative about updating. Don't want to modify timestamps... or do i?
            readsAdded = readsAdded.append(existingUpdate)
#             .loc[idx] = row ##record which Read_Set was assigned to these reads
        return readsAdded

    def addReadsToInvenotry(self,newReads):
        pass
    
    def addAssembliesToInventory(self,newAss):
        pass
    
    def ingestBAMbyLinkage(self,assembliesAdded):
        utilities.safeMakeDir(self.BAM_directory)
        if 'BAM_File' in assembliesAdded.columns:
            for _, row in assembliesAdded[assembliesAdded.BAM_File.notnull()].iterrows():
                src = row.loc['BAM_File']
                map_ext = os.path.splitext(src)[1].lstrip('.')
                base_ID = getBaseID(row.loc['Lab_ID'], row.loc['Version'])
                dest = os.path.join(self.BAM_directory,"{}.{}".format(base_ID,map_ext))
                try:
                    os.link(src,dest) 
                except IOError:
                    print("Unable to link mapping file. Trying to copy instead...\n\t"+dest)
                    try:
                        copyfile(src,dest)
                    except IOError:
                        print("Unable to copy mapping file... \n\t" + dest)        
    

################ Traditional Method-based with Globals ###################
###Set globals
#pylint: disable=W0601


def setRepositoryPaths(new_repository,ingestion=False):
    global Repository,RepoAssemblyDir,RepoReadDir,RepoAssemblyInvFile,RepoContigInvFile,RepoReadInvFile,RepoReadMapFile
    Repository = os.path.abspath(new_repository)
    if ingestion:
        utilities.safeMakeDir(Repository)
    RepoAssemblyDir = os.path.join(Repository,ASSEMBLY_DIR_REPO)
    if ingestion:
        utilities.safeMakeDir(RepoAssemblyDir)
    RepoReadDir = os.path.join(Repository,READ_DIR_REPO)
    if ingestion:
        utilities.safeMakeDir(RepoReadDir)
    RepoAssemblyInvFile = os.path.join(RepoAssemblyDir,INVENTORY_FILE_BASE)
    RepoContigInvFile = utilities.appendToFilename(RepoAssemblyInvFile,'_contigs')
    RepoReadInvFile = os.path.join(RepoReadDir,INVENTORY_FILE_BASE)
    RepoReadMapFile = os.path.join(RepoAssemblyDir,READMAP_FILE)

chksum_prefix = 'Adler32_'

#Required means that the input file must have this field
##Fields can only be int if they are guaranteed to exist in every sample
inventoryHeadersFrame = pd.DataFrame(columns=['Field','dtype','Required','Recommended','Updatable'],data=[
('Lab_ID',str,True,True,False),
('Version',int,False,False,False),
('Filename',str,True,True,False),
('BAM_File',str,False,True,False),
('Project',str,False,True,True),
('Date_Created',str,False,False,False), ##Can be cast with pd.to_datetime,False), but apparently not with astype
('Date_Ingested',str,False,False,False),
('Technology',str,True,True,True),
('Assembler',str,False,True,True),
('BaseCaller',str,False,True,True),
('Person Performing Analysis',str,True,True,True),
('Institution Performing Analysis',str,True,True,True),
('Gaps',bool,False,True,True),
('Contig_Count',int,False,False,False),
('Bases_In_Contigs',int,False,False,False),
('Large_Contig_Count',int,False,False,False),
('Small_Contig_Count',int,False,False,False),
('Bases_In_Large_Contigs',int,False,False,False),
('Bases_In_Small_Contigs',int,False,False,False),
('Mean_Depth_of_Coverage',float,False,True,True),
('Reference_Assembly',str,False,True,True),
('Original_Filename',str,False,False,False),
(chksum_prefix+'Filename',str,False,False,False),
('Active',bool,False,False,True),
('Invalid',bool,False,True,True),
('Notes',str,False,True,True)                                    
])


inventoryHeaders = [x for x in inventoryHeadersFrame['Field'].tolist()]
reqAssFields = inventoryHeadersFrame['Required']
inventoryHeadersRequired = [x for x in inventoryHeadersFrame[reqAssFields]['Field'].tolist()]
recAssFields = inventoryHeadersFrame['Recommended']
inventoryHeadersRecommended = [x for x in inventoryHeadersFrame[recAssFields]['Field'].tolist()]
updateAssFields = inventoryHeadersFrame['Updatable']
inventoryHeadersStatic = [x for x in inventoryHeadersFrame[~updateAssFields]['Field'].tolist()]

inventoryContigHeaders = ['Invalid','Notes','Ambiguous','Version','Lab_ID']

readAssemblyMapFrame = pd.DataFrame(columns=['Field','dtype','Required'],data=[
    ('Lab_ID',str,True),
    ('Read_Set',int,True),
    ('Assembly_Version',int,True),
    ('Notes',str,False),         
    ])                                                                               
                                                                               
readAssemblyMapHeaders =  [x for x in readAssemblyMapFrame['Field'].tolist()]
# ['Lab_ID','Assembly_Version','Read_Set','Notes'] ##There is no natural key field in this table

readInventoryHeadersFrame = pd.DataFrame(columns=['Field','dtype','Required','Recommended'],data=[
    ('Lab_ID',str,True,True),
    ('Read1',str,False,True),
    ('Read2',str,False,True),
    ('Read_Set',int,False,False),
    ('Original_Read1',str,False,False),
    ('Original_Read2',str,False,False),
    ('Institution Performing WGS',str,True,True),
    ('Person Performing WGS',str,True,True),
    ('Technology',str,True,True),
    ('Machine_Class',str,False,True),
    ('Machine_ID',str,False,True),
    ('Reaction_Parameters',str,False,True), #e.g. read length, chemistry
    ('Project',str,False,True),
    ('Notes',str,False,True),
    ('Date_Created',str,False,False),
    ('Date_Ingested',str,False,False),
    ('Invalid',bool,False,True),
    (chksum_prefix+'Read1',str,False,False),
    (chksum_prefix+'Read2',str,False,False)           
    ])

readInventoryHeaders = [x for x in readInventoryHeadersFrame['Field'].tolist()]
reqReadFields = readInventoryHeadersFrame['Required']
readInventoryHeadersRequired = [x for x in readInventoryHeadersFrame[reqReadFields]['Field'].tolist()]
recReadFields = readInventoryHeadersFrame['Recommended']
readInventoryHeadersRecommended = [x for x in readInventoryHeadersFrame[recReadFields]['Field'].tolist()]

#for Notes
readHeaderShortcuts = {'Institution':'Institution Performing WGS',
                   'Person':'Person Performing WGS'} 
assHeaderShortcuts = {'Institution':'Institution Performing Analysis',
                   'Person':'Person Performing Analysis'} 

# dfHeaders = ['Lab_ID','Filename']
readFileKeys = ['Read1','Read2']
assFileKeys = ['Filename','BAM_File']

# read_data_fileHeaders = ['Lane','Sample ID','Index','Yield (Mbases)','# Reads','% Perfect Index Reads','% of >= Q30 Bases (PF)','Mean Quality Score (PF)']

def vprint(text):
    if _verbose:
        print(text)
  
    
############ Organizing Mening Lab datasets
########## Transferred to NGS_data_utilities ########################

##Looks for a Meningitis lab sample identifier (M#) in the filename. Currently uses the strict definition ("M" plus 5 digits).
# Returns empty string if fails

########## Transferred to NGS_data_utilities ########################
# def guessNameFromGenomeFile(filename):
#     return NGS_data_utilities.guessNameFromGenomeFile(filename)

####### This is the core function for identifying genomes in a directory
##Returns dataframe with header of.##Also saves the DF to file in case it needs to be reviewed/edited

########## Transferred to NGS_data_utilities ########################
# def listGenomeFilesWithNames(directory,outfile = None, deep_search = True):
#     return NGS_data_utilities.listGenomeFilesWithNames(directory,outfile, deep_search)

##Copy the assembly file to a new location, with a simple name and simple contig identifiers    
### Try to keep the same contig ID numbers and keep them in the same order in the file

## Need a way to match up the unpaired read files that arise from filtering of reads

# r1 = 'R1'
# r2 = 'R2'
# read_codes = [r1,r2]
# def listReadFilesWithNames(directory,outfile = None,read_extension=read_ext):
#     return NGS_data_utilities.listReadFilesWithNames(directory,outfile,read_extension)

# def mergeReadDataFile(filename):
    
    
# def openReadDataFile(filename):
#     return NGS_data_utilities.openReadDataFile(filename)


                
# def pairReads(fileList):
#     return NGS_data_utilities.pairReads(fileList)
# 
# def parseIlluminaNames(filename):
#     return NGS_data_utilities.parseIlluminaNames(filename)
# #             vprint(readInfo[filename])

######## END transfer to NGS_data_utilities ###############3

##Deprecated?
def listAssembliesWithReads(assemblyDir, readDir, outfile = None):
    if (assemblyDir is not None) and os.path.isdir(assemblyDir):
        assFrame = NGS_data_utilities.listGenomeFilesWithNames(assemblyDir)
    else:
        assFrame = None
        if assemblyDir:
            print("{} is not a directory.".format(assemblyDir))
    if (readDir is not None) and os.path.isdir(readDir):
        readFrame = NGS_data_utilities.listReadFilesWithNames(readDir)
    else:
        readFrame = None
        if readDir:
            print("{} is not a directory.".format(readDir))
    if not (assFrame is None or readFrame is None):
        finalFrame = pd.merge(assFrame,readFrame,how='outer')
    elif assFrame is not None:
        finalFrame = assFrame
    elif readFrame is not None:
        finalFrame = readFrame
    else:
        print("No Data!")
        return None
    if outfile is not None:
        finalFrame.to_csv(outfile,sep='\t',index=False)
    return finalFrame
     
def moveToStandardizedAssemblyFile(genome_file,sample_name,output_directory="./",version = 0,compress=True):
    try:
        utilities.safeMakeDir(output_directory)
    except IOError:
        print("Failed to make output directory: {}".format(output_directory))
        raise
    (genome_format,compressed) = utilities.guessFileFormat(genome_file)
    new_filename = None
    if genome_format is not None: 
        base_ID = getBaseID(sample_name,version)
        try:
            if compressed:
                with gzip.open(genome_file,'rt') as fin:
                    contig_list = [x for x in SeqIO.parse(fin,genome_format)]            
            else:
                with open(genome_file) as fin:
                    contig_list = [x for x in SeqIO.parse(fin,genome_format)]
        except IOError:
            print("Failed to read genome file: {}".format(genome_file))
            raise
        if len(contig_list) == 0:
            print("Error in file {}: failed to read genome file. Check extension for implied format".format(genome_file))
            return None
        new_contigs, c = seq_utilities.standardize_contig_names(contig_list,base_ID)
        if c > 0:
            print("Re-numbered {} contigs in assembly {}".format(c,base_ID))
        new_filename = os.path.join(output_directory,"{}.{}".format(base_ID,genome_format))
        if compress: 
            new_filename += '.gz'
        if not os.path.exists(new_filename):
            if compress:
                with gzip.open(new_filename,'wt') as fout:
                    SeqIO.write(new_contigs,fout,genome_format)
            else:
                with open(new_filename,'wt') as fout:
                    SeqIO.write(new_contigs,fout,genome_format)
            os.chmod(new_filename, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH) #Read only
        else:
            print("Unable to save file {} because of prexisting file with same name".format(new_filename))
            new_filename = None
    else:
        print("Failed to identify format for genome file: "+genome_file)
        print("Please use an extension in this list : {}".format(utilities.format_guesser))
    return new_filename
    
#Update the inventory file so that it includes the read files that were used to assemble each genome
############## NOT COMPLETE ######################

# def linkGenomeToReads(inventory_file,genome_path,reads_path,read_destination=None):
#     if os.path.isfile(inventory_file):
#         inventory = pd.read_table(inventory_file)
#     else:
#         print("Inventory file is not valid. Exiting")
#         print(inventory_file)
#     return None
    
#Returns inventory dataframe
## The inventory does not have the "Filename" field that is in the genome_frame

def moveListedGenomes(genome_frame,destination_dir,inventory_file,field_dict=None,extract_info=True):
    assert isinstance(genome_frame,pd.DataFrame)
    assert field_dict is None or isinstance(field_dict,dict)
    assert isinstance(inventory_file,str)
    assert isinstance(extract_info,bool)
    utilities.safeMakeDir(destination_dir) ##Will throw error if directory cannot be created
    ##Validate list of assemblies
    if genome_frame is None:
        raise Exception("No genome frame")
    genome_frame_trimmed = genome_frame[genome_frame['Lab_ID'] != ''].copy()
    diff = len(genome_frame) - len(genome_frame_trimmed)
    if diff > 0:
        vprint("Unable to move {} files because no sample name is identified".format(diff))
    #Get exsiting inventory for versioning and appending
    inventory_dir = os.path.dirname(inventory_file)
    if os.path.isfile(inventory_file):
        inventory = pd.read_table(inventory_file,dtype=str)
        inventory_path_join = functools.partial(os.path.join,inventory_dir)
        for c in assFileKeys:
            if c in inventory.columns:
                good_values = inventory[c].notnull()
                inventory.loc[good_values,c] = inventory[good_values][c].apply(inventory_path_join) # pylint: disable=no-member
    else:
        inventory = pd.DataFrame(columns=inventoryHeaders)
    ##Add the notes to the incoming list
    if field_dict is not None:
        for header,value in field_dict.items():
            genome_frame_trimmed[header] = value
    ## Make a new name for the file in the repository
    pre_inv = pd.DataFrame(columns=inventoryHeaders)
    for f,g in genome_frame_trimmed.groupby('Filename'):
        g = g.copy()
        sample_name = g['Lab_ID'].unique().tolist()[0] ##TODO: error check that labID is consistant for Filename
        tempFrame = inventory[inventory['Lab_ID'] == sample_name].append(pre_inv[pre_inv['Lab_ID'] == sample_name],ignore_index=True)
        version = 0 if len(tempFrame) == 0 else int(tempFrame['Version'].max()) + 1
        file_name = f
        if not os.path.isfile(file_name):
            print("File does not exist: {}".format(file_name))
            continue
        try:
            g['Date_Created'] = time.ctime(os.path.getctime(file_name))
        except OSError:
            print("ERROR: failed to read creation date from file {}".format(file_name))        
            continue                                         
        else:
            g['Date_Ingested'] = time.ctime()
        try:
            new_name = moveToStandardizedAssemblyFile(file_name,sample_name,destination_dir,version)
        except IOError:
            new_name = None
        if new_name == None:
            print("ERROR: failed to move file {}".format(file_name))
        else:            
            g['Version'] = str(version)
            g['Filename'] = new_name
            g['Original_Filename'] = file_name
        for _, row in g.iterrows():            
            pre_inv = pre_inv.append(row,ignore_index=True)

    pre_inv = calcChecksums(pre_inv,assFileKeys,validation=False)
    #~ temp_filename = utilities.appendToFilename(inventory_file,'temp')
    #~ utilities.safeOverwriteCSV(temp_filename,inventory,sep='\t',index=False)    
    if extract_info:
        (pre_inv, contig_inventory) = extractAssemblyStats(pre_inv,inventory_dir) #make contig inventory
        ##Establish standard headers even if they are currently empty
        cols = contig_inventory.columns.values
        for col in inventoryContigHeaders:
            if col not in cols:
                contig_inventory[col] = ''
        contig_filename = utilities.appendToFilename(inventory_file,'_contigs')
        if os.path.isfile(contig_filename):
            old_contigs = pd.read_table(contig_filename)
            contig_inventory = old_contigs.append(contig_inventory)
        utilities.safeOverwriteCSV(contig_filename,contig_inventory,sep='\t',index=False)
    ##Make the final inventory set
    inventory = inventory.append(pre_inv.drop_duplicates(subset=['Lab_ID','Version']))
    ##Mark genome "Active" if unique and not Invalid -- otherwise notify user of need to choose one
    prospective = (inventory['Active'] != False) & (~inventory['Active'].isin(['False','FALSE','0'])) & (inventory['Invalid'] != True) #Cannot be previously passed up
    inventory.loc[~prospective,'Active'] = False ##Assures that all Invalid assemblies are also marked not Active
    lab_ids = inventory[prospective]['Lab_ID']
    dup_list = lab_ids[lab_ids.duplicated()].tolist()
    dups = inventory['Lab_ID'].isin(dup_list)
    inventory.loc[prospective & ~dups,'Active'] = True
    ##Reorder the columns and save to file
    cols = inventory.columns
    extra_cols = [c for c in cols if c not in inventoryHeaders]
    inventory = inventory[inventoryHeaders + extra_cols]
    ## Relative filepaths
    ass_rel_path = functools.partial(os.path.relpath,start=inventory_dir)
    for c in assFileKeys:
        if c in inventory.columns:
            good_values = inventory[c].notnull()
            inventory.loc[good_values,c] = inventory[good_values][c].apply(ass_rel_path)# pylint: disable=no-member
    utilities.safeOverwriteCSV(inventory_file,inventory,sep='\t',index=False)
    ### Report duplicate assemblies so that user can select which one is "active"
    duplicates = inventory[prospective & dups].copy() ##Todo: this appears to be selecting some that are already inactive. Don't know why.
    if len(duplicates) > 0:
        dup_count = len(duplicates['Lab_ID'].unique())
        print("#####\nNew sequences introduced for {} genomes for which alternative sequences are in the database. Designate some as Active\n########".format(dup_count))
        duplicates = duplicates[inventoryHeaders].sort_values(by='Lab_ID') ##Limit it to standard headers for readability. Can always go to the inventory file for full info.]
        dupFile = os.path.join(inventory_dir,'inventory_duplicates_choose_Active.tab')
        try:
            utilities.safeOverwriteCSV(dupFile,duplicates,sep='\t',index=False)
            print("Duplicates are listed in "+dupFile) 
        except IOError:
            print("Failed to write table of duplicated assemblies at {}.".format(dupFile))         
        
    return pre_inv
    
    ###NOTE: getOriginal not implemented ##########
    ###### Not tested ###########


#Copy read files to repository, and return a data frame with updated information about the read
def moveListedReads(read_frame,destination_dir):
    moved_reads = pd.DataFrame(columns=read_frame.columns)
#     cols = [col for col in read_frame.columns.tolist() if "Read" in col]
#     assert len(cols) > 0
    for idx, row in read_frame.iterrows():
#         file_time = ''
        for c in readFileKeys:
            source = row[c]
            if pd.notnull(source) and source != '':
                dest = os.path.abspath(os.path.join(destination_dir,os.path.basename(source)))
                if os.path.exists(dest):
                    print("Warning: file {} already exists. \n\tNot importing from {}".format(dest,source))
                    ####### ToDo: Grab the old_inv and report the row for the existing data so that it can be linked to assembly 
                else:
                    transferred = False
                    try:
                        if re.match('http',source):
                            urllib.request.urlretrieve(source,dest) ##Untested
                            transferred = True
                        elif os.path.isfile(source):
#                             file_time = time.ctime(os.path.getctime(source)) #should be identical for paired files
                            try:
                                copyfile(source,dest)
                                transferred = True
                            except IOError:
                                print("ERROR: Unable to write to {}".format(dest))
                        else:
                            vprint("Not a read file: {}".format(source))
                    except Exception:
                        print("Warning: exception while transferring file {}. \n\tNot importing from {}".format(dest,source))
                    if transferred: #read file transferred to destination dir
                        row[c] = dest #os.path.relpath(dest,destination_dir)##Handled upon saving: Note: this assumes that the inventory file is in the reads directory
                        ##This should already be assigned... but I guess it's safe to keep it here to make sure nothing gets mixed up
                        orig = "Original_{}".format(c)
                        if orig not in moved_reads.columns:
                            moved_reads[orig] = ''
                        row[orig] = source
    #                     if 
    #                     read_inv.append(pd.Series([row['Lab_ID'],dest],readInventoryHeaders)) #Lab_ID and Filename
#         row.loc['Date_Created'] = file_time
#         row.loc['Date_Ingested'] = time.ctime()
        moved_reads.loc[idx] = row #keep the original indicies
    return moved_reads

##newFrame should already have basic inventory format
def mergeReadsWithInventory(newFrame):
    update_Inv, _ = readSetup(RepoReadInvFile, RepoReadDir,ValidOnly=False)
#     if os.path.isfile(RepoReadInvFile):
#         update_Inv = pd.read_table(RepoReadInvFile)
#     else:
#         update_Inv = pd.DataFrame(columns=newFrame.columns)
    for idx, row in newFrame.iterrows():
        row.loc['Read_Set'] = str(sum(update_Inv['Lab_ID'] == row['Lab_ID']))
        update_Inv = update_Inv.append(row,ignore_index=True)
        newFrame.loc[idx] = row ##record which Read_Set was assigned to these reads
    return update_Inv, newFrame
    
##TODO this needs to be incorporated into the InventoryReader -- the directories will be messed up otherwise
    
# def exportSelectedGenomes(inventorySelectionFrame,inventoryFile_Dir,destination_dir,output_compress=True,output_format='fastq',getOriginal=False,edge_trim=0,strict_contig=False,contigInvFrame=None):
#     assert isinstance(inventorySelectionFrame,pd.DataFrame)
#     assert os.path.isdir(inventoryFile_Dir)
#     assert output_format in utilities.format_guesser.keys()
#     assert edge_trim >= 0
#     have_contigs = isinstance(contigInvFrame,pd.DataFrame)
#     if have_contigs:
#         assert 'Contig_Name' in contigInvFrame.columns
#         CIF = contigInvFrame.set_index('Contig_Name')
#     else:
#         assert not strict_contig  ##Must have a contig inventory in order to enforce strict contig selection
#     utilities.safeMakeDir(destination_dir)
#     for _, row in inventorySelectionFrame.iterrows():
#         if getOriginal:
#             filename = row.loc['Original_Filename'] ###Untested. Will only work on filesystem where consolidation was done
#         else:            
#             filename = row.loc['Filename']
#             filename = os.path.join(inventoryFile_Dir,filename)
#         (genome_format,compressed) = utilities.guessFileFormat(filename)
#         
#         (_,name) = os.path.split(filename)
#         dest_file = os.path.join(destination_dir,name)
#         ##Test the destination
#         if os.path.exists(dest_file):
#             dest_file = utilities.appendToFilename(filename,"_"+time.strftime("%Y%m%d%H%M%S"))
#             if os.path.exists(dest_file):
#                 print("Cowardly refusing to overwrite file: "+dest_file)
#                 print("Failed to export: "+filename)
#         ##Could call ExportGenomeFasta
#         if (output_format == genome_format) and (edge_trim == 0) and (not strict_contig): ##No need to modify contents
#             if output_compress == compressed:
#                 copyfile(filename,dest_file)
#             else: ##Simple decompress
#                 with gzip.open(filename,'rt') as fin:
#                     with open(dest_file,'wt') as fout:
#                         fout.writelines(fin) 
#         else: 
#             with utilities.flexible_handle(filename,compressed,'rt') as fin:
#                 with utilities.flexible_handle(dest_file,output_compress,'wt') as fout:
#                     for contig in SeqIO.parse(fin,genome_format):
#                         keep_contig = True
#                         if strict_contig: ##
#                             keep_contig = not CIF['Ambiguous']
#                         if keep_contig:
#                             if edge_trim>0:
#                                 contig = seq_utilities.trimFASTQtoFirstBase(contig,edge_trim)
#                             SeqIO.write(contig,fout,output_format)  
            
### Note, could extract above code for more flexible function          

# def genomeOrganizer.extractActiveAssembly(genome_name,temp_genome,output_compress=True,output_format='fastq',getOriginal=False,edge_trim=0,strict_contig=False,contigInvFrame=None,repository)  
#             
def exportGenomeFASTA(genome_file,export_file,file_format = '',is_compressed = None, include_qual = False):
    ##Setup export
    destination_dir =  os.path.dirname(export_file)
    utilities.safeMakeDir(destination_dir)
    ##Get info about necessary manipulations
    if file_format == '':
        (genome_format,genome_compressed) = utilities.guessFileFormat(genome_file)
    else:
        genome_format = file_format
        genome_compressed = is_compressed 
    ##Convert if needed
    if genome_format != 'fasta' or genome_compressed:
        with utilities.flexible_handle(genome_file,genome_compressed,'rt') as fin:   
            with open(export_file,'wt') as fout:
                if genome_format != 'fasta':
                    SeqIO.write(SeqIO.parse(fin,genome_format),fout,'fasta')
                    if include_qual:
                        raise "Do This"  #TODO: Export Qual
                else:
                    fout.write(fin.read())
    else:
        try:
            copyfile(genome_file,export_file)
        except IOError:
            print("ERROR: Unable to write to {}".format(export_file))
         
def exportReadFrame(rf,destination,linked=True,InventoryOnly=False):
    utilities.safeMakeDir(destination)
    if not InventoryOnly:
        exported_rows = []
        for _,r in rf.iterrows():
            Fail = False
            rs = r.Read_Set
            lid = r.Lab_ID
            read_set = '{}_rs{}'.format(lid,rs)
            read_count = 0
            src1 = r.Read1
            if isinstance(src1,str) and os.path.isfile(src1):
                base1 = os.path.basename(src1).replace(lid,read_set)
                dest1 = os.path.join(destination,base1)
                read_count += 1
            src2 = r.Read2
            if isinstance(src2,str) and os.path.isfile(src2):
                base2 = os.path.basename(src2).replace(lid,read_set)
                dest2 = os.path.join(destination,base2)
                read_count += 1
            if read_count == 2:
                if linked:
                    try:
                        os.link(src1,dest1) 
                        os.link(src2,dest2)
                    except IOError:
                        print("Unable to link paired read. Maybe try copying instead?\n\t"+dest1)
                        linkFail = True
                if not linked or linkFail:
                    try:
                        copyfile(src1,dest1)
                        copyfile(src2,dest2)
                    except IOError:
                        print("Unable to copy paired reads... \n\t" + dest1)
                        Fail = True
            elif read_count == 1:
                print("Error: Found a single read file. Not exporting single reads.")
                Fail = True
            elif read_count == 0:
                print("Error: Found no read files for {} set {}. Probably a SMRT Portal URL".format(lid,rs))
                Fail = True
            r['Read1'] = dest1 if not Fail else 'None'
            r['Read2'] = dest2 if not Fail else 'None'
            r['RepositoryRead1'] = src1 ##Just for reference
            r['RepositoryRead2'] = src2
            exported_rows.append(r)
        rf = pd.DataFrame(exported_rows) ##Use updated names in exported inventory
    read_file = os.path.join(destination,INVENTORY_FILE_BASE)       
    utilities.safeOverwriteTable(read_file, rf,'tab',index=False)                
                
###DEPRECATE: move to Assembly Stats
## Returns a dictionary reporting the number of bases in CONTIG that fall below thresholds defined in QUAL_TARGETS 
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

############ Not Tested ################
##InventoryFrame is updated, and returns a contig inventory if requested
###These variables are moved to AssemblyStats
qual_targets = [20,30,40,50] #Cutoff qualities for reporting low-quality bases; needs to be increasing, because we want values lower than (or equal to) target
quality_head = "Bases_Under_Q"
def extractAssemblyStats(inventoryFrame,inventoryDir=None):
    ### This is important, but for some reason this may return an "Int64Index" which does not have this function
#     assert not inventoryFrame.index.has_duplicates(), 'Cannot extract assembly stats on data frame with non-unique values'
    master_contig_inventory = pd.DataFrame()
#     for f,g in inventoryFrame.groupby('Filename'):
#         filename = f
#         g = g.copy()    
    for idx, row in inventoryFrame.iterrows():
        filename = row.loc['Filename']
        if not os.path.isabs(filename) and inventoryDir is not None:
            filename = os.path.join(inventoryDir,filename)
        if os.path.isfile(filename):
            (genome_format,compressed) = utilities.guessFileFormat(filename)
            assert (compressed) or (inventoryDir is None), 'Always compressed in consolidated directory'
            with utilities.flexible_handle(filename,compressed,'rt') as fin: 
                contig_list = [x for x in SeqIO.parse(fin,genome_format)]     
            if len(contig_list) > 0:                
                ## Get stats for contigs into dataframe.
                contigFrame = getContigStats(contig_list,hasQual = (genome_format == 'fastq'))      
                assert len(contig_list) == len(contigFrame), "Not all contigs are in dataframe"                
                ##Link these contigs to the assembly
                if "Lab_ID" in row:
                    contigFrame['Lab_ID'] = row['Lab_ID']
                if "Version" in row:
                    contigFrame['Version'] = row['Version']  
                ##Update the assembly record         
                inventoryFrame.loc[idx,'Contig_Count']=str(len(contig_list))
                contigSizes = contigFrame['Contig_Size'].astype(int)
                assemblySize = sum(contigSizes)
                inventoryFrame.loc[idx,'Bases_In_Contigs'] = str(assemblySize) 
                largeContigs = contigSizes > 10000
                inventoryFrame.loc[idx,'Large_Contig_Count'] = str(sum(largeContigs))
                inventoryFrame.loc[idx,'Small_Contig_Count'] = str(sum(~largeContigs))
                inventoryFrame.loc[idx,'Bases_In_Large_Contigs'] = str(sum(contigSizes[largeContigs]))
                inventoryFrame.loc[idx,'Bases_In_Small_Contigs'] = str(sum(contigSizes[~largeContigs]))
                    ## Import the quality scores
                for c in contigFrame.columns:
                    if c.startswith(quality_head):
                        inventoryFrame.loc[idx,c] = str(sum(contigFrame[c]))            
                    ##Calculate N50 and N90
                N_stats = calcN50_stats(contigSizes.tolist())
                for n,size in N_stats.items():
                    header = "N{}".format(n)
                    inventoryFrame.loc[idx,header] = str(size)
                ##Add to inventory frame
                master_contig_inventory.append(contigFrame,ignore_index=True)
            else:
                print("Error in assembly inventory. No contigs in file {}".format(filename))
        else:
            print("Error in assembly inventory. Cannot find file {}".format(filename))
    return inventoryFrame, master_contig_inventory ##TODO: find more elegant solution for examining files twice

###DEPRECATE: this has been moved to AssemblyStats. Call that package...
def getContigStats(contig_iterator,hasQual):
    contig_records = []
    for contig in contig_iterator:
        ##### Quality scores
        if hasQual:
            qual = contig.letter_annotations["phred_quality"]  
            qual_threshold = bin_quality_scores(qual,qual_targets)
        else:
            qual_threshold = defaultdict(int) #only modified by fastq
        ##Record contig-specific measures,
        this_record = { 'Contig_Name':contig.id,
                        'Contig_Size':str(len(contig))
                        }
        if len(qual_threshold) > 0: ##TODO: test this with PacBio data
            for i in qual_threshold.keys():
                header = quality_head + "{}".format(i)
                this_record[header] = qual_threshold[i]
        contig_records.append(this_record)
    ##Record whole-genome traits
    return pd.DataFrame(contig_records,dtype=str)     

####DEPRECATE: move to Assembly Stats        
def calcN50_stats(size_list, thresholds = None):
    if thresholds is None:
        thresholds = [50,90]
    assert max(thresholds) < 100, "Cannot calcualte N100 or greater"
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
        
##TODO: this will calculate twice if a file is listed twice (as in when muliple read sets are used fro assembly)        
def calcChecksums(dataFrame,file_fields,validation=True): ##By default, do not modify table
    newFrame = pd.DataFrame(columns = dataFrame.columns,index = dataFrame.index)
#     newFrame = dataFrame[dataFrame.index.isnull()].copy()
    ##Add the checksum fields
#     chk_fields = ['Adler32_'+x for x in file_fields]
    if not validation:
        for x in file_fields:
            newFrame[chksum_prefix+x] = ''
    ##Calculate checksums
    for idx, row in dataFrame.iterrows():
        for x in file_fields:
            if x in dataFrame.columns:
                url = row[x]
                if pd.notnull(url) and url != '':
                    if not re.match('http',url):
                        filename = url
                        if os.path.isfile(filename):
                            cksum_name = chksum_prefix+x
                            oldsum = row[cksum_name] if cksum_name in row else None
                            if pd.notnull(oldsum) or not validation:
                                with open(filename,'rb') as fin:
                                    chksum = zlib.adler32(fin.read())
                                if validation:
                                    if oldsum != str(chksum):
                                        print("Error: invalid checksum on file: {}".format(filename)) 
                                else:
                                    row[cksum_name] = str(chksum)
                        else:
                            print("Warning! Missing file {}".format(filename))
        try:
            newFrame.loc[idx] = row
        except Exception:
            print("Unable to add {} to {} at {}".format(row,newFrame,idx))
            raise
    return newFrame

import argparse

##Note: all_isolates_fasta will bypass htis 
def get_isolates_from_args(args,inventory=None):
    use_file = bool(args.isolate_file)
    use_list = args.isolates and (len(args.isolates) > 0)
    isolates = []
    if args.all_isolates_fasta:
        if use_file or use_list:
            sys.exit("Nonsensical isolate selection: cannot export all and a specific list too")
        else:
            assert inventory is not None
            assert isinstance(inventory, Inventory)
            return inventory.assembly_frame['Lab_ID'].unique().tolist()
    if use_file:
        with open(args.isolate_file,'rt') as isolate_in:
            for x in isolate_in:
                isolates += x.strip().split()
        print("Exporting files for {} genomes listed in {}".format(len(isolates),args.isolate_file))       
    if use_list:
        print("Exporting files for {} genomes listed on command line".format(len(args.isolates)))
        isolates = isolates + args.isolates
    return isolates
    
    
def extract(extract_args):
    #Check that repository exists -- redundant with InventoryReader
    if os.path.isdir(Repository):
        setRepositoryPaths(Repository)
    else:
        print("Invalid Repository: {}\n".format(Repository))
        return 1
    ### Open inventory 
    inventory = InventoryReader(Repository)
    if not inventory.valid:
        return 1    
    ### Get isolate list
    isolates = get_isolates_from_args(extract_args,inventory)
    if len(isolates) == 0:
        print("No genomes requested. Exiting")
        return 1
    ### Set export
    export_dir = extract_args.target_directory if extract_args.target_directory else os.path.join(os.getcwd(),"GenomeData_"+time.strftime("%Y%m%d%H%M%S"))
    export_dir = os.path.realpath(export_dir)
    utilities.safeMakeDir(export_dir)
    print("Exporting genome data to {}".format(export_dir))
    ActiveOnly = False if extract_args.all_versions else True
    if extract_args.all_isolates_fasta:
        remaining_reads = inventory.getReadsWithoutAssembly()
        read_filename = os.path.join(export_dir,'unassembled_reads.tab')
        utilities.safeOverwriteTable(read_filename, remaining_reads, 'tab')
    if not extract_args.reads_only:
#         ass_dir = os.path.join(export_dir,'assemblies') if extract_args.reads_also else export_dir
#         utilities.safeMakeDir(ass_dir)
        exportedAssemblies = inventory.exportAssemblies(isolates,export_dir,ActiveOnly=ActiveOnly)
    if extract_args.reads_only:
        inventory.exportReads(isolates,export_dir)
#     elif extract_args.reads_also:
#         for _,row in exportedAssemblies.iterrows():
#             pass
            ##TODO: this should look up the linked read and export it ... or maybe teh BAM file someday.
#         print('Not implemented. Run again with "reads_only"')
            ##TODO: decide how to report the linkage between reads and assemblies
#

#             print("Exporting {} assembly files".format(len(assInv)))
#             edge_trim = 15 if extract_args.trim_edges else 0
#             output_format = 'fasta' if extract_args.fasta else 'fastq' 
#             if extract_args.strict_contig_filter:
#                 contigInvFrame = pd.read_table(RepoContigInvFile)
#             else:
#                 contigInvFrame = None
#             exportSelectedGenomes(assInv,os.path.dirname(RepoAssemblyInvFile),extract_args.target_directory,
#                                   output_compress=not extract_args.decompress,
#                                   output_format = output_format,
#                                   edge_trim=edge_trim,
#                                   strict_contig=extract_args.strict_contig_filter,
#                                   contigInvFrame=contigInvFrame)
#             print("Finished exporting assembly files")
#             export_inventory = os.path.join(extract_args.target_directory,INVENTORY_FILE_BASE)
#             utilities.safeOverwriteCSV(export_inventory,assInv,sep='\t',index=False)
#             if edge_trim or extract_args.strict_contig_filter:
#                 with open(export_inventory,'r+t') as inv_file:
#                     content = inv_file.read()
#                     inv_file.seek(0,0)
#                     inv_file.write('###The statistics in this file reflect the Repository file, not any modifications made during extraction' + '\n' + content)
#         else:
#             print("Unable to export assemblies due to absence of inventory file")
#     ##Get read data
#     if extract_args.reads_only or extract_args.reads_also:
#         readInv = pd.read_table(RepoReadInvFile)
#         readInvDir = os.path.dirname(RepoReadInvFile)
#         if extract_args.reads_only:
#             ##Get all reads associated with LabID
#             readInv = readInv[readInv['Lab_ID'].isin(isolates)]
#             readDir = export_dir
#         else:
#             ##assInv should be defined above
#             lab_ID = readInv['Lab_ID'].isin(assInv['Lab_ID'])
#             ass_version = readInv['Assembly_Version'].isin(assInv['Version'])
#             isSelected = lab_ID & ass_version
#             readInv = readInv[isSelected]
#             readDir = os.path.join(export_dir,READ_DIR_REPO)
#             print("Read extraction is not yet implemented")
#         utilities.safeMakeDir(readDir)
#         #######Export########
#         for _,row in readInv.iterrows():
#             for r in readFileKeys:
#                 source = row[r]
#                 dest = os.path.join(readDir,os.path.basename(source))
#                 if re.match('http',source):
#                     urllib.request.urlretrieve(source,dest) ##Untested
#                 else:
#                     source = os.path.join(readInvDir,source)
#                     copyfile(source,dest)
#         #####################
#         print("Finished exporting read files")
#         readInvFile = os.path.join(readDir,INVENTORY_FILE_BASE)
#         readInvFile = utilities.appendToFilename(readInvFile,'_reads')
#         utilities.safeOverwriteCSV(readInvFile,readInv,sep='\t',index=False)
    return 0

def submit(submit_args):
    #Check that repository exists -- redundant with InventoryReader
    if os.path.isdir(Repository):
        setRepositoryPaths(Repository)
    else:
        print("Invalid Repository: {}\n".format(Repository))
        return 1
    ### Get isolate list
    isolates = get_isolates_from_args(submit_args)
    if len(isolates) == 0:
        print("No genomes requested. Exiting")
        return 1
    ### Set export
    export_dir = submit_args.target_directory if submit_args.target_directory else os.path.join(os.getcwd(),"GenomeData_"+time.strftime("%Y%m%d%H%M%S"))
    utilities.safeMakeDir(export_dir)
    inventory = InventoryReader(Repository)
    if not inventory.valid:
        return 1
    inventory.exportAssemblies(isolates,export_dir,ActiveOnly=True,include_qual=True) ##TODO: export qual 


def ingest(ingest_args):
    def dump_and_exit(extraFrame=None,extraName='',realPath=True): ##Should probably rename "dump" since it does not exit on its own... (must call return)
        ##Establish location to dump error reports
        if ingest_args.report_location:
            dump_basename = ingest_args.report_location + '_ingest'
        else:
            dump_basename = os.path.join(os.getcwd(),"AbortedIngest")
        ass_dump= utilities.appendToFilename(dump_basename, '_assemblies')
        reads_dump = utilities.appendToFilename(dump_basename,'_reads')
        bam_dump = utilities.appendToFilename(dump_basename, '_bam')   
        merged_dump = utilities.appendToFilename(dump_basename,'_merged')  
        extra_dump = utilities.appendToFilename(dump_basename, extraName)
        ##Notify user
        if ingest_args.report_location:
            print("Writing aborted import information to requested report location...")
        else:
            print("Writing aborted import information to current directory...")
        print("\t"+dump_basename) 
        ##Dump
        if extraFrame is not None:
            utilities.safeOverwriteTable(extra_dump, extraFrame,'tab',index=False)
        if samFrame is not None:   
            utilities.safeOverwriteTable(bam_dump, samFrame, 'tab',index=False)
        if assFrame is not None:
            utilities.safeOverwriteTable(ass_dump, assFrame, 'tab',index=False)
        if readFrame is not None:
            utilities.safeOverwriteTable(reads_dump, readFrame,'tab',index=False)
        if ingest_args.reads_to_assembly:
            keys = ['Lab_ID']
            rc_rename = {r:'Reads_{}'.format(r) for r in readFrame.columns if r not in keys}
            readFrame.rename(columns=rc_rename,inplace=True)
            mergeExport = pd.merge(assFrame,readFrame,on=keys)      
            if realPath:
                for c in readFileKeys + assFileKeys:
                    if c in mergeExport.columns:
                        not_null = mergeExport[c].notnull() #& mergeExport[c].apply(os.path.isfile)
                        mergeExport.loc[not_null,c] = mergeExport[not_null][c].apply(os.path.realpath)           
            utilities.safeOverwriteTable(merged_dump,mergeExport,'tab',index=False)                
            
#             for c in assFileKeys:
#                 if c in assembly_frame.columns:
#                     good_values = assembly_frame[c].notnull()
#                     assembly_frame.loc[good_values,c] = assembly_frame[good_values][c].apply(inventory_path_join)         
        print("Exiting")
        return 1

    ##Initialize main variables
    readsAdded = readFrame = samFrame = None
    assFrame = assAdded = None
    mergedReadAss = None                
    ### Test for legitimate comibnations of Ingest files
    legit_args = True
    if ingest_args.assembly_guide and ingest_args.combined_guide:
        legit_args = False
        print("Cannot provide both an assembly guide and a combined guide.")
    require_reads = (len(ingest_args.read_notes) > 0) or ingest_args.reads_to_assembly or ingest_args.copy_read_files
    have_reads = ingest_args.read_directory or ingest_args.combined_guide
    ##TODO: this may have bugs in Read_Set is given rather than read filenames
    if require_reads and not have_reads:
        legit_args = False
        print("You have provided arguments that require reads but have not provided the reads themselves")
    require_assemblies = ingest_args.assembly_notes or ingest_args.assembly_extension or ingest_args.reads_to_assembly or ingest_args.sam_directory or ingest_args.sam_subdirectory
    have_assemblies = ingest_args.assembly_directory or ingest_args.assembly_guide or ingest_args.combined_guide
    if require_assemblies and not have_assemblies:
        legit_args = False
        print("You have provided arguments that require assemblies but have not provided the assemblies themselves")
    if ingest_args.sam_subdirectory and not ingest_args.assembly_directory:
        legit_args = False
        print("To search for BAM/SAM files, you must include an assembly directory.")
    if ingest_args.assembly_guide:
        if not os.path.isfile(ingest_args.assembly_guide):
            legit_args = False
            print("Assembly guide is not a file")
    if ingest_args.combined_guide:
        if not os.path.isfile(ingest_args.combined_guide):
            legit_args = False
            print("Combined guide is not a file")    
    if not legit_args:
        return 1    
    ##Make repository if necessary
    setRepositoryPaths(Repository,True)
    inventory = InventoryWriter(Repository) 
    if not inventory.valid:
        return 1   
    #### Convert Note lists to dictionary (validating the format)
    try:
        read_notes = {t[0] : t[1] for t in [item.split("=") for item in ingest_args.read_notes]}
        for key,replace in readHeaderShortcuts.items():
            if key in read_notes:
                read_notes[replace] = read_notes.pop(key)
        assembly_notes = {t[0] : t[1] for t in [item.split("=") for item in ingest_args.assembly_notes]}
        for key,replace in assHeaderShortcuts.items():
            if key in assembly_notes:
                assembly_notes[replace] = assembly_notes.pop(key)
    except:
        print("Error: Failed to parse the notes. Exiting")
        raise    
    ##Establish DataFrames for the imported files
    invTemplate = pd.DataFrame(columns = readInventoryHeaders)
    if ingest_args.combined_guide:   
#         print(ingest_args.combined_guide)
        try:
            guideFrame = pd.read_table(ingest_args.combined_guide)
        except IOError:
            print("Cannot open the guide file. Exiting")
            raise   
#         print (guideFrame.columns)         
        guideFrame.dropna(how='all',inplace=True)
        read_col_regex = re.compile(r"(Read[s12]?)([ _](.*)|$)?")
        read_cols = ['Lab_ID'] #Need Lab_ID in both readFrame and assFrame
        ass_cols = []
        renamed_cols = read_cols.copy()
        for c in guideFrame.columns.tolist():
            read_match = read_col_regex.match(c)
            if read_match:
                read_cols.append(c)
                if c in['Reads','Read']:
                    renamed_cols.append("Read1") ##Better not have two columns!!
                else:
                    m_groups = read_match.groups()# 1 "Read[]", 2 optional suffix, 3 content of suffix
                    if m_groups[2] is None:
                        new_name = m_groups[0]
                    else:
                        new_name = m_groups[2]                    
                    renamed_cols.append(new_name) ##Don't rename ## TODO: strip "reads" prefix from name -- use the match
            else:
                ass_cols.append(c)
        assFrame = guideFrame[ass_cols].copy()
        readFrame = guideFrame[read_cols].copy() ##Frames will have same index
        readFrame.columns = renamed_cols #TODO this will leave some messy field names, but I don't think we can universally remove "Read" from the beginning of each field
    if readFrame is None and ingest_args.read_directory:
        readFrame = NGS_data_utilities.listReadFilesWithNames(ingest_args.read_directory,read_extension=ingest_args.read_extension) #Read1 and Read2 for paired reads; Read1 for unpaired. 
        if readFrame is None:
            print("Failed to identify any reads in "+ingest_args.read_directory)
            print("Exiting")
            return 1
        ##Organize columns so that standard fileds come first
        readFrame = readFrame.append(invTemplate)
        cols = readInventoryHeaders + [c for c in readFrame.columns if c not in readInventoryHeaders]
        readFrame = readFrame[cols].copy()                  
    if ingest_args.sam_directory:
        sam_dir = ingest_args.sam_directory 
        if os.path.isdir(sam_dir):
            samFrame = NGS_data_utilities.listSAMFilesWithNames(sam_dir)
        else:
            print("{} is not a directory.".format(sam_dir))
    assembly_has_ReadSet = False
    if assFrame is None: ##TODO: this treats the combined guide and the assembly guide inconsistantly
        assemblyDir = ingest_args.assembly_directory
        if assemblyDir:
    #         genome_frame = listAssembliesWithReads(ingest_args.assembly_directory,read_dir,ingest_args.assemblyInListFile)
            print("Identifying genome assembly files in {}".format(assemblyDir))
            if os.path.isdir(assemblyDir):
                deep_search = False if ingest_args.shallow_search_assemblies else True
                assFrame = NGS_data_utilities.listGenomeFilesWithNames(assemblyDir,deep_search = deep_search)
                if assFrame is None or len(assFrame) == 0:
                    print("Failed to find assemblies in "+assemblyDir)
            else:
                print("{} is not a directory.".format(assemblyDir))
            if ingest_args.sam_subdirectory:
                tempSamFrame = NGS_data_utilities.listSAMFilesWithNames(assemblyDir, None, True)
                samFrame = samFrame.append(tempSamFrame) if samFrame is None else tempSamFrame
        assemblyGuide = ingest_args.assembly_guide
        if assemblyGuide:
            print("Reading assembly guide file: {}".format(assemblyGuide))
            if os.path.isfile(assemblyGuide):
                guideFrame = pd.read_table(assemblyGuide,comment='#').dropna(how='all')
                assembly_has_ReadSet = 'Read_Set' in guideFrame.columns
                if assembly_has_ReadSet:
                    if any(guideFrame.Read_Set.isnull()):
                        print("Assembly guide file has 'Read_Set' column, but some fields are empty. Cannot proceed.")
                        return 1
                else: ##Assembly files can be listed twice only if they are reporting two read sets
                    dups = sum(guideFrame['Filename'].duplicated())
                    if dups > 0:
                        print("Some files are listed twice in the guide file -- aborting")
                        return 1
            if assFrame is None:
                assFrame = guideFrame
            else:
                old_sum = len(assFrame) + len(guideFrame)
                assFrame = pd.merge(assFrame,guideFrame,how='outer',on='Filename')
                if old_sum != len(assFrame):
                    print("Found {} duplicates between the guide file and the directory. Aborting".format(old_sum - len(assFrame)))
                    return 1 
    ###Merge SAM field:
    if (samFrame is not None) and (assFrame is not None):
        updateFrame = NGS_data_utilities.mergeAssWithSam(assFrame,samFrame)
        valid_sams = NGS_data_utilities.validateAssSamMatch(updateFrame)        
        if valid_sams:
            assFrame = updateFrame
        else:
            return dump_and_exit(updateFrame,'BAM_Assembly')
    ##Before doing anything, make sure that required fields are in readFrame, assemblyFrame
    ### First, add the notes
    for header,value in read_notes.items(): ##Remainder are Header=Value pairs for all records in directory      
        readFrame[header] = value  
    for header,value in assembly_notes.items():
        assFrame[header] = value     
    assembly_notes = None      
    ##Transfer shared columns
#     shared_cols = ['Project','Technology'] ##Not sure how to do this without risk of overwriting something    
    ##Test required fields        
    field_error = "Error: not all records contain all required fields\n"  
    if isinstance(assFrame,pd.DataFrame):
        if set(inventoryHeadersRequired) <= set(assFrame.columns):
            trim_table = assFrame[inventoryHeadersRequired].copy()
            invalid_records = trim_table.isnull().any(axis=1)
            if sum(invalid_records) > 0:
                print(field_error + "\tAssembly frame has {} invalid records".format(sum(invalid_records)))
                field_error = ''
        reqAssSet = set(inventoryHeadersRequired)
        realAssSet = set(assFrame.dropna(axis=1,how='any').columns.tolist())
        missingAssSet = reqAssSet - realAssSet
    else:
        missingAssSet = set()
    if isinstance(readFrame,pd.DataFrame):
        readsExisting, readsNew = inventory.compareWithExistingReads(readFrame)
        if len(readsNew) > 0:        
            if set(readInventoryHeadersRequired) <= set(readFrame.columns):
                trim_table = readFrame[readInventoryHeadersRequired].copy()
                invalid_records = trim_table.isnull().any(axis=1)
                if sum(invalid_records) > 0:
                    print(field_error+"\tRead frame has {} invalid records".format(sum(invalid_records)))
                    field_error = ''
            reqReadSet = set(readInventoryHeadersRequired)
            realReadSet = set(readFrame.dropna(axis=1,how='any').columns.tolist())
            missingReadSet = reqReadSet - realReadSet
        else: 
            missingReadSet = set() ##No new reads
    else:
        missingReadSet = set()
    if len(missingAssSet) > 0 or len(missingReadSet) > 0:
        if len(missingAssSet) > 0:
            print(field_error+"\tAssembly guide is missing the following fields: {}".format(missingAssSet))
            field_error = ''
        if len(missingReadSet) > 0:
            print(field_error+"\tRead guide is missing the following fields: {}".format(missingReadSet))
            field_error = ''      
        if not ingest_args.override_fields: ##Provide a guide file to work with
            ##First add the required fields
            if assFrame is not None:
                for c in inventoryHeadersRecommended:
                    if c not in assFrame.columns:
                        assFrame[c] = None
                assFrame = assFrame[inventoryHeadersRecommended].copy()
            if readFrame is not None:
                for c in readInventoryHeadersRecommended:
                    if c not in readFrame.columns:
                        readFrame[c] = None
                keep_headers = readInventoryHeadersRecommended
                keep_headers += [x for x in NGS_data_utilities.read_data_fileHeaders if (x in readFrame.columns) and (x not in keep_headers)] 
                readFrame = readFrame[keep_headers].copy()
            ##Then export in appropriate format               
            return dump_and_exit()
    ########################## Updating starts here ####################3
    ##Import reads ######################  Replace this with InventoryWriter???  Already have inventory object
    if readFrame is not None:
        ##Mark all reads as "original" location even if not moved to new location
        for c in readFileKeys:
            orig = "Original_{}".format(c)
            readFrame[orig] = readFrame[c]
        readsExisting, readsNew = inventory.compareWithExistingReads(readFrame)
        vprint("Found {} existing reads and {} new reads".format(len(readsExisting),len(readsNew)))
        if ingest_args.copy_read_files:########## TRANSFER #
            print("Transferring reads to repository")
            readsNew = moveListedReads(readsNew, RepoReadDir)
            readsNew = calcChecksums(readsNew,readFileKeys,validation=False)
        readsAdded = inventory.mergeReadsWithInventory(readsNew,readsExisting) ##ReadsAdded is just the preInv with the "Read_Set" column
#         inventory.update_reads_fromFile(readsExisting) ##TODO figure out how to import the Excel data for the reads without messing up table
#         inventory.saveReadInventory()
        utilities.safeOverwriteCSV(RepoReadInvFile,readPackup(inventory.read_frame,RepoReadDir),sep='\t',index=False)
        print("Updated read inventory")                        
    if assFrame is not None and len(assFrame) > 0:
        print("Moving {} assembly files into the repository".format(len(assFrame.Filename.unique())))
        assAdded = moveListedGenomes(assFrame,RepoAssemblyDir,RepoAssemblyInvFile,assembly_notes,extract_info=True)
        inventory.ingestBAMbyLinkage(assAdded) ##This adds files to BAM directory in repository, but does not modify inventory table
    elif assemblyDir or assemblyGuide or ingest_args.combined_guide:
        print("No genomes files. Exiting")
        return 1
    if ingest_args.reads_to_assembly or ingest_args.combined_guide or assembly_has_ReadSet:
        if assAdded is None:
            print("Cannot map reads to assemblies without both reads and assemblies. Aborting")
            return 1
        print("Creating link between reads and assemblies")
        if ingest_args.combined_guide:
            mergedReadAss = pd.merge(assAdded,readsAdded,left_index=True,right_index=True,on='Lab_ID') #Lab_ID is shared; using index avoids duplication
        elif assembly_has_ReadSet:
            mergedReadAss = assAdded.copy()
        elif readsAdded is not None:
            mergedReadAss = pd.merge(assAdded,readsAdded,on='Lab_ID')
        else:
            print("Cannot map reads to assemblies without both reads and assemblies. Aborting")
            return 1            
        
        cols = mergedReadAss.columns.tolist() ##Change header for mepping list
        i = cols.index("Version")
        cols[i] = "Assembly_Version" 
        mergedReadAss.columns = cols
        mergedReadAss['Notes'] = ''
        mergedReadAss = mergedReadAss[readAssemblyMapHeaders]
        if os.path.isfile(RepoReadMapFile):
            old_readmap = pd.read_table(RepoReadMapFile)
            mergedReadAss = old_readmap.append(mergedReadAss)
        utilities.safeOverwriteCSV(RepoReadMapFile, mergedReadAss, index=False,sep='\t')
        print("...linked...")
    ##Report what was added
    if ingest_args.report_location:
        basename = ingest_args.report_location
        if assAdded is not None:
            ass_added_name = utilities.appendToFilename(basename, '_assemblies')
            utilities.safeOverwriteTable(ass_added_name, assAdded, 'tab')
        if readsAdded is not None:
            reads_added_name = utilities.appendToFilename(basename,'_reads')
            utilities.safeOverwriteTable(reads_added_name, readsAdded,'tab')
        if mergedReadAss is not None:
            merged_name = utilities.appendToFilename(basename,'_linkage')
            utilities.safeOverwriteTable(merged_name,mergedReadAss,'tab')
    ##export the versioned assembly files
    if ingest_args.export_folder:
        utilities.safeMakeDir(ingest_args.export_folder)
        readFolder = None if readsAdded is None else ingest_args.export_folder if assAdded is None else os.path.join(ingest_args.export_folder,READ_DIR_REPO)
        assFolder = None if assAdded is None else ingest_args.export_folder if readsAdded is None else os.path.join(ingest_args.export_folder,ASSEMBLY_DIR_REPO)
        if assAdded is not None:
            exportFrame = assAdded.rename(columns={'Filename':'Repository_File'}).drop_duplicates('Repository_File')
            for idx, row in exportFrame.iterrows():
                baseID = getBaseID(row['Lab_ID'],row['Version']) #Lab_ID and Version
                tech = row['Technology'] if pd.notnull(row['Technology']) else "TechUnavail"
                baseID += '_' + tech
                dest_filename = os.path.abspath(os.path.join(assFolder,baseID) + '.fasta')
                exportGenomeFASTA(row['Repository_File'],dest_filename)
                exportFrame.loc[idx,'Filename'] = dest_filename
            utilities.safeOverwriteTable(os.path.join(assFolder,'ingested_inventory.tab'),exportFrame,'tab',index=False)     
        if readsAdded is not None:
            exportReadFrame(readsAdded, readFolder)
    return 0

def validate(validate_args): 
    inventory = InventoryReader(Repository)
    if not inventory.valid:
        return 1
    #Check that repository exists
#     if os.path.isdir(Repository):
#         activateRepository(Repository)
#     else:
#         print("Invalid Repository: {}\n".format(Repository))
#         return 1
#     #################3
#     if os.path.isfile(RepoReadInvFile):
    print("Starting validation of read files")
#     readFrame = pd.read_table(RepoReadInvFile)
    calcChecksums(inventory.read_frame,readFileKeys,validation=True)
    print("Finished validating read files")
        ##ToDo: reverse check -- match files to inventory
        ##Use checksum to identify duplicate files (and Lab_ID)
#     else:
#         print("No read inventory in repository: {}".format(Repository))
#     if os.path.isfile(RepoAssemblyInvFile):
    print("Starting validation of assembly files")
#     assFrame = pd.read_table(RepoAssemblyInvFile)
    calcChecksums(inventory.assembly_frame,assFileKeys,validation=True)
    print("Finished validating assembly files")
    ##ToDo: reverse check -- match files to inventory
    ##Use checksum to identify duplicate files
#     else:
#         print("No assembly inventory in repository: {}".format(Repository))
    #ToDo: CHeck for multiple "active" assemblies; assure that no invalids are marked active
    
    ##ToDo: check that the Lab_ID matechs the filename for reads
    return 0

def update(update_args):
    ##Open repository
    inventory = InventoryWriter(Repository)
    if not inventory.valid:
        return 1
    updated = False
    ##Modify inventories.
    if update_args.assembly_updater:
        if not os.path.isfile(update_args.assembly_updater):
            return 1
        else:
            if inventory.update_assemblies(update_args.assembly_updater):
                print("updated assembly inventory")
                updated = True
            else:
                print("Nothing done to read inventory.")
    if update_args.read_updater:
        if not os.path.isfile(update_args.read_updater):
            return 1
        else:        
            if inventory.update_reads_fromFile(update_args.read_updater):
                print("Updated read inventory")
                updated = True
            else:
                print("Nothing done to read inventory.")
    ##Save inventories
    if updated:
        inventory.saveInventoryFiles()
        rf = inventory.linkInvalidAssToReads() ##This will reload the saved inventory (with invalids)
        if len(rf) > 0:
            print("Invalid assemblies are linked to unmarked reads. ")
            updateFile = os.path.join(inventory.repository,'reads_linked_to_invalid_assembly.tab')
            utilities.safeOverwriteTable(updateFile, rf, 'tab',index=False)        
    return 0
        
    
setting_options = ['repository']
SETTING_FILE = 'GO_settings.txt'
SETTING_PATH = os.path.join(SCRIPT_DIR,SETTING_FILE) 
   
import configparser
def get_default_settings(setting_file,debug=False):
    
    try:
        config = configparser.ConfigParser()
        config.read(setting_file)
    except:
        result = None
        print("Failure to read setting file. {}".format(setting_file))
    else:
        if debug:
            result = config['DEBUG']
        else:
            homedir = os.environ['HOME']
            if homedir in config:
                result = config[homedir]
            else:
                result = config['DEFAULT']
    return result
#         
#     if os.path.isfile(setting_file): 
#         try:
#             with open(setting_file) as settings_in:
#                 settings_dict = dict([line.split() for line in settings_in])
#         except IOError:
#             
#         return settings_dict
#     else:
#         print("No default setting file at"+setting_file)
#         return None
#         

def main():
    print("")
    print("Running {} from {} at {}".format(SCRIPT_NAME,os.getcwd(),time.ctime()))
    print("...script and settings are found in {}\n".format(SCRIPT_DIR)) 
    
    parser = argparse.ArgumentParser(description='A program to consolidate and standardize genome data files.',
                                     epilog='Settings are defined by the file {}. Each line must have the parameter and then a space. The options are: {}'.format(SETTING_PATH,",".join(setting_options)),
)
#                                      ,formatter_class=argparse.MetavarTypeHelpFormatter)
    ##Info
    parser.add_argument('--version','-V',action='version',version='%(prog)s {}.{}'.format(script_version,script_subversion))
    parser.add_argument('--debug',action='store_true',help='Create a temporary repository in current directory')
    parser.add_argument('--repository','-R',help='Directory containing genome Repository (has e.g. "assemblies" and "reads" as possible subdirectories')
    subparsers = parser.add_subparsers(description="Select one of the following commands",dest='subcommand')
    subparsers.required = True
    
    ##Extract  
    extract_parser = subparsers.add_parser('extract',description="Retrieve data files from the archive")
    extract_parser.set_defaults(func=extract)
    isolate_group = extract_parser.add_argument_group("Isolate selection",'Provide one or more of these options')
    isolate_group.add_argument('--isolate_file','-if',help='Location of a file listing the desired isolates (one per line)')
    isolate_group.add_argument('--isolates','-i',nargs='*',help='A list of isolates to retrieve (space-separated)')
    isolate_group.add_argument('--all_isolates_fasta',action='store_true',default=False)
    extract_parser.add_argument('--target_directory','-t',help='Location to write the extracted files to. Default is current directory')
    extract_parser.add_argument('--decompress',action='store_true',help='Decompress genome files. Will be g-zipped by default')
    read_group = extract_parser.add_mutually_exclusive_group()
#     read_group.add_argument('--reads_also',action='store_true',help='Also extract the read files that is associated with the assembly as g-zipped FASTQ')
    read_group.add_argument('--reads_only',action='store_true',help='Extract all read files for this isolate as g-zipped FASTQ; ignore assembly files')
    extract_parser.add_argument('--fasta',action='store_true',help='Convert to FASTA format. Default is FASTQ')
    extract_parser.add_argument('--strict_contig_filter',action='store_true',help='Remove contigs that are marked as possibly spurious in inventory file')
    #TODO: allow user to set this value
    extract_parser.add_argument('--trim_edges','-e',action='store_true',help='Removes low-quality bases (<Q15) from edges of contigs.')
    extract_parser.add_argument('--all_versions',action='store_true',help='Extract all assembly versions for the listed isolates')
    
    ##Submission
    submission_parser = subparsers.add_parser('NCBI_submit',description="Retrieve files from the achive, formatted for NCBI submission")
    submission_parser.set_defaults(func=submit)
    submission_parser.add_argument('--organism','-o',help='Organism identifier for submission (e.g. species binomial)')
    submission_parser.add_argument('--gcode','-g',help='Genetic code identifier from NCBI. Default is Bacterial (11)',default=11,type=int)
    sub_isolate_group = submission_parser.add_argument_group("Isolate selection",'Provide one or more of these options')
    sub_isolate_group.add_argument('--isolate_file','-if',help='Location of a file listing the desired isolates (one per line)')
    sub_isolate_group.add_argument('--isolates','-i',nargs='*',help='A list of isolates to retrieve (space-separated)')
    submission_parser.add_argument('--target_directory','-t',help='Location to write the extracted files to. Default is current directory')


    ##Ingest
    ingest_parser = subparsers.add_parser('ingest',description="Move data files into the archive")
    ingest_parser.set_defaults(func=ingest) 
    ## Input options
    input_group = ingest_parser.add_argument_group("Input options",'Provide one or more of these options')
    input_group.add_argument('--assembly_directory','-ad',help='A directory containing genome assembly files to organize (e.g. standardize nomenclature and collect in the repository)')
    input_group.add_argument('--shallow_search_assemblies',help='Do not search subdirectories for assemblies',action='store_true')
    input_group.add_argument('--read_directory','-rd',help='A directory containing genome read files that will be inventoried.')
    input_group.add_argument('--sam_directory','-sd',help='A directory containing SAM/BAM files with reads mapped to the assemblies.')
    input_group.add_argument('--sam_subdirectory',action='store_true',help='Look in SAM/BAM files in assembly directory or its subdirectories.')
    input_group.add_argument('--assembly_guide','-ag',help='A tab-delimited table listing the assembly files to organize, along with additional information to be recorded in inventory file')
    input_group.add_argument('--combined_guide','-cg',help='A tab-delimited table listing the assembly files to organize under "Filename", the reads under "Reads" or "Read1" and "Read2", along with additional information to be recorded in inventory file. Notes fro the Read file are prefixed with the word Read')
    input_group.add_argument('--export_folder','-ef',help='A folder to export the assemblies and reads to (creates subfolders if needed)')
#     input_group.add_argument('--read_guide','-rg',help='A tab-delimited table listing the read files to inventory, along with additional information to be recorded in the inventory')
    
#     parser.add_argument('--assemblyInListFile','-aif',help='File in which to save the list of assembly files that are inventoried')
#     parser.add_argument('--readInListFile','-rif',help='File in which to save the list of read files that are inventoried')
    ingest_parser.add_argument('--copy_read_files',action='store_true',help='Copy read files to repository. Otherwise the inventory will point to the current files')
    ingest_parser.add_argument('--reads_to_assembly',action='store_true',help='Match the read files to the assembly files based on Lab_ID, and record them as the reads that were used to call bases in the assemblies')
    ingest_parser.add_argument('--assembly_notes','-an',nargs='*',default=[],
                                        help='Additional notes to add to the inventory table for all records, in the form HEADER=VALUE.\
                                            Standard header values include: {}'.format("; ".join(inventoryHeaders)))
    ingest_parser.add_argument('--read_notes','-rn',nargs='*',default=[],
                                        help='Additional notes to add to the inventory table for all reads, in the form HEADER=VALUE.\
                                            Standard header values include: {}'.format("; ".join(readInventoryHeaders)))
    ingest_parser.add_argument('--read_extension','-re',help='the file extension that identifies the reads',default=read_ext)
    ingest_parser.add_argument('--assembly_extension','-ae',help='the file extension that identifies the assemblies. Not implemented')
    ingest_parser.add_argument('--paired_reads',action='store_true',help='Indicate that the reads are paired')
    ingest_parser.add_argument('--report_location','-rl',help='A filename to export the new tables to')
    ingest_parser.add_argument('--override_fields',action='store_true',help="Override the required fields for assembly and read notes")
    
    ##Validate
    validate_parser = subparsers.add_parser('validate',description='Will check that files have not been modified')
    validate_parser.set_defaults(func=validate)
    validate_parser.add_argument('--remove_files',help='Remove assembly files that are not listed in the inventory (move to new directory)')
    
    ##Update inventory
    update_parser = subparsers.add_parser('update',description='Will modify inventory using tables provided, specifying Lab_ID,Version pairs to update')
    update_parser.set_defaults(func=update)
    update_parser.add_argument('--assembly_updater','-a',help='The provided records will be updated in the inventory')
    update_parser.add_argument('--read_updater','-r',help='The provided records will be updated in the inventory')
    
    args = parser.parse_args()
    
    ##Setablish the basic settings
    debug = False
    if args.debug:
        global _verbose
        _verbose = True #Implicitly global
        debug = True
    
    global Repository
    if args.repository:
        Repository = args.repository
    else:
        settings_dict = get_default_settings(SETTING_PATH,debug)
        Repository = settings_dict['repository']
        
   
        
    ##Run the program
    result = args.func(args)
    if result != 0:
        parser.print_usage()
        if args.subcommand is not None:
            parser.parse_args([args.subcommand,'-h'])
#         subparser_name = args['subparser_name']
#         if subparser_name == update:
#             update_parser.pr
        
    
    ### Finish by copying the primary inventory files to the home directory so that people can look at them:
    tempInventory = InventoryReader(Repository)
    if tempInventory.valid:
        tempInventory.duplicateInventoryFiles(Repository)
        ### Put warning in Repository directory
        warning_file = os.path.join(Repository,"DO_NOT_TOUCH_THE_SUBDIRECTORIES")
        try:
            open(warning_file, 'a').close()
        except IOError:
            pass
        ### Return error value (particularly from validate)
        print("Finished")
    else:
        print("Unable to update inventory files in repository root due to invalid inventory")
    sys.exit(result)
    



    

    
if __name__ == "__main__":
    if not utilities.has_preferred_python():
        raise Exception("Upgrade your python version")
    main()

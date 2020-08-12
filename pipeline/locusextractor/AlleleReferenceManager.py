import os
import re
import pandas as pd
import urllib.request
import sys
# from glob import glob
import shutil
import utilities
import seq_utilities
from _collections import defaultdict
from Bio import SeqIO

# LocusTableMask = 'locus_list*.tab'
LocusTableFile = 'locus_list.tab'
# LocusTableColumns = ['locus','isORF','isPeptide','basename','URL','expected','species']
LocusTableEssential = ['locus','URL']
true_values=['True','TRUE','Yes']
LocusTableBoolColumns = ['isORF','isPeptide','expected']

referenceSubdirectory = 'reference_sequences/' ##This should be a subdirectory somewhere
### This retrieves all the information from PubMLST, and provides the allele sequences files when requested.
## I am putting lookup tables in a separate object, but the MLST table is still here. I can't decide whether to extract it so that it is kept with 
## other lookup tables or whether it should stay here because it is actively retrieved from the PubMLST site.
script_version = 0.15  #9 Sept 2015
script_subversion =0

def readAlleleReferences(filename):
    alleles = {}
    if os.path.isfile(filename):
        refDir = os.path.dirname(filename)
        alleles = dict()
        try:
            with open(filename) as fin:
                for line in fin:
                    if line[0] != '#':
                        (gene,allele_file) = line.rstrip().split('\t') ##Filename is relative to local_allele_file
                        alleles[gene] = os.path.join(refDir,allele_file)
        except IOError:
            print("Warning: unable to open local allele master file: {}".format(filename))  
    return alleles
    
##Setting dir is where to find information about alleles to use
## Reference Dir is place to store downloaded alleles (perhaps to be deprecated)
## Output dir is a place to keep a permanent copy of the references used in this analysis
reqUpdate='RequireUpdate'
class AlleleReferenceManager:
    def __init__(self,settingDir,referenceDir):        
        ##Location of settings
        self.setting_directory = settingDir 

        ##Basic information about the loci to evaluate
        LocusFrameRaw = pd.read_table(os.path.join(settingDir,LocusTableFile),comment='#',dtype=str) 
        LocusFrameRaw.set_index(keys='locus',inplace=True,drop=False,verify_integrity=True)
        LocusFrameRaw = utilities.castColumnsToBool(LocusFrameRaw,LocusTableBoolColumns,true_values)
        self.LocusFrame = LocusFrameRaw.dropna(subset=LocusTableEssential,how='any')
        dif = len(LocusFrameRaw) - len(self.LocusFrame)
        if dif > 0:
            print("Dropping {} loci due to missing information. Check settings file".format(dif))
        if len(self.LocusFrame) == 0:
            print("Error: no loci identified")
#         if reqUpdate in self.LocusFrame:
            
#         print("Evaluating {} sequences".format(len(self.LocusFrame)))
        self.allele_data = dict()    

        self.MLST_profile_file = os.path.join(settingDir,"MLST_profiles.txt")

        #store a master copy of allele files here; keep as backup
        self.reference_directory = referenceDir
        if not os.path.isdir(self.reference_directory):
            os.mkdir(self.reference_directory)
                 
        ##TODO check if this ever should be replaced with a version in the working dir
        self.local_allele_file = self.reference_directory + 'allele_reference.txt'
        self.local_profile_file = self.reference_directory + 'MLST_reference.txt'
        self.MLST_schemes = dict()
        
        #Tell main program to wait if necessary
        self.updated = False ##For tracking if there was background updating
        
    def updateReferences(self, waitForCompletion = True, EssentialOnly = False):
    ##At some point, there will be a thread in here and the option to not wait for completion

        ### Read the URLs for allele reference files; Retrieve them if they are not local
#         with open(self.allele_references_file) as allele_file:
#             allele_lines = allele_file.readlines()
#         allele_references = dict([line.split() for line in allele_lines if line != ''])
        ######### Note: handle blank lines better
        remote_references = False
        for URL in self.LocusFrame['URL']:
            if not os.path.isfile(URL):
                remote_references = True
                break                    
               
        #### Keep track of genes that have reference files
        if remote_references:
            print(" Updating reference files...\n")
            local_references = self.downloadAlleleReferences(EssentialOnly)
            

## TODO: should this be in load references?
        #if a gene does not have a user-specified basename, try to infer it from the file
        # Attempted to make this compatible with both PubMLST.org conventions and MLST.org conventions. 
        # This search will fail if the allele name has anything but numbers in it (or if the gene name ends with a number).
        names_updated = False
        nameRE = re.compile(r'>(.*\D)\d+$')
        for (gene, filename) in local_references.items():
            if gene in self.LocusFrame.index and not pd.isnull(self.LocusFrame.loc[gene,'basename']): ##test that the name works
                with open(filename) as fin:
                    for line in fin:
                        if re.match(">",line):
                            if not re.match(">"+self.LocusFrame.loc[gene,'basename'],line):
                                raise RuntimeError('Specified basename for {} is inconsistant with usage in allele file'.format(gene))
            else: 
                names_updated = True
                name = None
                with open(filename) as fin:
                    for line in fin:
                        nameMatch = nameRE.match(line)
                        if nameMatch:
                            new_name = nameMatch.group(1)
                            if name == None:
                                name = new_name
                            elif name != new_name:
                                raise RuntimeError('Inconsistant naming in file {}; {} and {}.'.format(filename,name,new_name))
                
                self.LocusFrame.loc[gene,'basename'] = name   
        if names_updated:
            out_file = os.path.join(self.setting_directory,"names_updated.tab")
            self.LocusFrame.to_csv(out_file,sep='\t')
            raise ValueError("You did not provide a key to permit interpretation of the names in the gene files. We made suggestions. Try replacing your locus list files with {}".
                                format(out_file))
                               

        #Get profiles
        local_profile_files = dict()
        with open(self.MLST_profile_file) as profiles:
            for line in profiles:
                values = line.split()
                URL = values[1]
                name = values[0]
                local_profiles = self.reference_directory + name + '_profiles.txt'
                if not (EssentialOnly and os.path.isfile(local_profiles)):
                    if EssentialOnly:
                        print('Cannot proceed without a MLST profile list for {}'.format(name))
                        print('To override automatic download, put a properly formatted profile list from PubMLST here:'.format(local_profiles))
                    print('Downloading MLST profile for {}'.format(name))
                    handle = urllib.request.urlopen(URL)
                    temp = local_profiles+'.tmp'
                    with open(temp,'wb') as fout:
                        fout.write(handle.read())
                    ##TODO: if local_profiles exists, we should check that temp is a good replacement. However, I don't know what qualifies as "good", since records could theoretically be removed legitimately                     
                    if name == 'Nm':
                        try:
                            self.reformatNmCC(temp,local_profiles)
                        except:
                            print("Warning: failed to reformat new MLST profile table at {}".format(temp))
                    else:
                        os.rename(temp,local_profiles)
                local_profile_files[name] = local_profiles
        #Save a list of the local reference files so that this can be used even if the server is down
        with open(self.local_profile_file,'w') as fout:
            local_dir = os.path.dirname(self.local_profile_file)
            for (gene, filename) in local_profile_files.items():
                file_dir,file_name = os.path.split(filename)
                rel_dir = os.path.relpath(file_dir,local_dir)
                rel_file = os.path.join(rel_dir,file_name)
                fout.write(gene + "\t" + rel_file + "\n") 

                
            
        ##THis is a logical placeholder for when the above code is threaded
        if waitForCompletion:
            self.updated = False ##
            #~ t = multiprocessing.Process(target=worker)
            #~ t.start()
            #~ t.join()
        else:
            print("Background updating not implemented yet")
            #~ t = threading.Thread(target=worker)
            #~ t.start()
            #~ self.updated = updateThread  ## The thread would need to 
            
    ##Takes a dict of address for the ultimate reference files (allele_references), downloads them, and saves the list in the "local_allele_file"
    def downloadAlleleReferences(self,EssentialOnly=False):
        downloaded_references = dict()
        ####Use the existing local references by default
        default_refs = readAlleleReferences(self.local_allele_file) 
        for gene in self.LocusFrame.index:
            if gene in default_refs:
                if os.path.isfile(default_refs[gene]):
                    downloaded_references[gene] = default_refs[gene]
        ##Try to download the files, or copy them from the setting directory to the reference directory
#         genes_remaining = set(self.LocusFrame.index.tolist())
#         if EssentialOnly:
#             genes_remaining = [x for x in genes_remaining if x not in downloaded_references]
#         for gene in genes_remaining:
        success = True
        for (gene, row) in self.LocusFrame.iterrows():
            url = row['URL']
#             url = self.LocusFrame.loc[gene,'URL']
            dest_file = os.path.normpath(os.path.join(self.reference_directory,gene+".fasta"))
            try:
                if os.path.isfile(url):
                    shutil.copyfile(url,dest_file)
                elif os.path.isfile(os.path.join(self.setting_directory,url)):
                    shutil.copyfile(os.path.join(self.setting_directory,url),dest_file)                
                else: ##Download
                    if (EssentialOnly and gene in default_refs): 
                        if os.path.abspath(dest_file) != os.path.abspath(default_refs[gene]):
                            shutil.copyfile(default_refs[gene],dest_file)
                    else:
                        if EssentialOnly:
                            print("{} not in local allele file: {}".format(gene,self.local_allele_file))
                        temp_file = dest_file+'.tmp'
                        handle = urllib.request.urlopen(url)
                        with open(temp_file,'wb') as fout:
                            fout.write(handle.read())
                        ##Validate
                        new_seqs = SeqIO.to_dict(SeqIO.parse(temp_file,'fasta')) 
                        if len(new_seqs) == 0:
                            raise ValueError('Failed to parse PubMLST download file for {}'.format(gene))        
                        failed_seq = None
                        if not os.path.isfile(dest_file): ##Confirm that old sequences are in the new file
                            print("Downloaded new sequence for {}".format(gene))
                        else:
                            old_seqs = SeqIO.to_dict(SeqIO.parse(dest_file,'fasta'))
                            for seq_name,seq in old_seqs.items():
                                if seq_name in new_seqs:
                                    if seq.seq != new_seqs[seq_name].seq:
                                        failed_seq = seq_name
                                        print("Old seq ({}bp) does not match new seq ({}bp)".format(len(seq),len(new_seqs[seq_name])))
                                        break
                                else:
                                    failed_seq = seq_name
                                    break
                            if failed_seq is None:
                                print("Validated new sequence for {}".format(gene))
                        if failed_seq is None:
                            os.rename(temp_file,dest_file) #only overwrite once download is complete
                        else:
                            print("Failed to validate new sequences for {}, due to absence of {}".format(gene,failed_seq))
                            print("The URL is: \n\t"+url)
                            with open(temp_file) as pubmlst_download:
                                line = pubmlst_download.readline()
                                print("The first line of the downloaded file is: \n\t"+line)
                            raise ValueError('Failed to validate PubMLST download file for {}'.format(gene))                        
            except ValueError as e:
                print('Download Error for {}; relying on backup file {}. Message : {}'.format(url,self.local_allele_file,e))
#                         genes_remaining.remove(gene)
                if not (reqUpdate in row.index) or (row[reqUpdate] in ['True','TRUE','Yes']):
                    success = False
                else:
                    print("Continuing, but you may want to see if newly downloaded file is usable:"+temp_file)
                
            else:
                downloaded_references[gene] = dest_file ##the exception will not get here
#             genes_remaining.remove(gene)
        #Save a list of the local reference files so that this can be used even if the server is down
        with open(self.local_allele_file,'w') as fout:
            local_dir = os.path.dirname(self.local_allele_file)
            for (gene, filename) in downloaded_references.items():
                file_dir,file_name = os.path.split(filename)
                rel_dir = os.path.relpath(file_dir,local_dir)
                rel_file = os.path.join(rel_dir,file_name)
                fout.write(gene + "\t" + rel_file + "\n")   
        if not success:
            sys.exit("Failure to download files. Fatal error. Run in --debug mode if you want to run without fresh download")                 
        return downloaded_references
            
            
    ##our database reformats the clonal complex names from pubmed
    ##This whole thing should be wrapped in a try block
    def reformatNmCC(self,file_in, file_out):
        profile_table = pd.read_table(file_in,header=0)
        cc_list = profile_table['clonal_complex'].unique()
        print("Loading profile table for {}. Has {} profiles in {} clonal complexes".format('Nm',len(profile_table),len(cc_list)))
        cc_re = re.compile('ST-((/?\d+)+) complex(.+)?')##'complex' may need to be stripped from end
        for idx, row in profile_table.iterrows():
            CC_ID = row['clonal_complex']
            if (CC_ID == '') or pd.isnull(CC_ID):
                CC_ID = 'unassigned CC for {}'.format(row['ST'])
            else:
                try:
                    cc_match = cc_re.match(CC_ID)
                    if cc_match:
                        refST = cc_match.group(1)
                        extraID = cc_match.group(3)
                        CC_ID = "CC"+refST
                        if extraID is not None:
                            CC_ID += extraID.replace('complex','').rstrip()
                    else:
                        print("Warning: unable to interpret the clonal complex for ST {}".format(row['ST']))
                except:
                    print('Exception while to reformatting {}'.format(CC_ID))
            profile_table.loc[idx,'clonal_complex'] = CC_ID #pylint: disable=no-member
        if os.path.exists(file_out):
            print("Warning: overwriting file {}".format(file_out))
        profile_table.to_csv(file_out,'\t',index=False)
        
    def backgroundUpdateOccured(self):
        ##This may need to aqcuire a lock on 'updated' so that it waits for the updating thread to complete
        raise Exception("Not implemented")
        return self.updated  ##This will return True if the analysis was performed prior to downloading the 
    

#         
#     def readAlleleRefNames(self,filename):
#         ## load user-defined basenames for allele identification files
#         allele_reference_name = dict()
#         if os.path.isfile(filename):
#             try:
#                 with open(filename) as fin:
#                     lines = fin.readlines()
#                 allele_reference_name = dict([line.rstrip().split('\t') for line in lines if line[0] != '#'])
#             except:
#                 print("Warning: unable to open basename file for reference alleles: {}".format(filename)) 
#         return allele_reference_name
        
    def readAlleleLookupTables(self,filename):
        lookup_tables = dict()
        if os.path.isfile(filename):
            try:
                lookup_tables = dict([line.rstrip().split('\t') for line in open(filename) if line[0] != '#'])
            except IOError:
                print("Warning: unable to open file for allele lookup tables: {}".format(filename)) 
        return lookup_tables
    
    
    def getAlleleFromQuery(self,locus,allele_name):
        query_file = self.getAlleleRefName(locus)
        allele_ID = self.extractAlleleID(locus, allele_name)
        with open(query_file) as query_handle: 
            query_seqs = SeqIO.to_dict(SeqIO.parse(query_handle, "fasta"))
            try:
                best_seq = query_seqs[allele_name]
            except KeyError:##This should never happen
                print("Failure to find query {} in sequence list {}. Contact developer".format(allele_name,query_file))
                raise
            my_seq = best_seq        
        return allele_ID,my_seq        
    
    def extractAlleleID(self,locus,allele_name):
        basename = self.getAlleleRefName(locus)
        allele_ID = None  
        try:
            allele_ID = re.search(basename+'(.+)$',allele_name).group(1)
        except Exception:
            print('Failure to identify {} in {}'.format(basename,allele_name))
        return allele_ID      
    

    def loadReferences(self,backupDir = None):
        ##Make backup copy
        if backupDir is not None:
            try:
                shutil.rmtree(backupDir)
                shutil.copytree(self.reference_directory,backupDir)
            except shutil.Error:
                print("Error: unable to make backup copy of references...")
        ##Alleles
        local_alleles = readAlleleReferences(self.local_allele_file)
        ##validate 
        gene_set = set(self.LocusFrame.index.tolist())
        local_set = set(local_alleles.keys())
        if local_set < gene_set:
            print("Error: local allele file has  only {}/{} alleles.".format(len(local_set),len(gene_set)))
        for gene, file in local_alleles.items():
            if gene in self.LocusFrame.index: ##Do not add new records to LocusFrame -- this is the master controller
                self.LocusFrame.loc[gene,'allele_sequences']  = os.path.normpath(file)          
                if self.LocusFrame.loc[gene,'isORF']: ##Only testing for internal stops
                    try:
                        analysis_dict = seq_utilities.ORF_analysis(file)
                        analysis_frame = pd.DataFrame(analysis_dict)
                        for i in analysis_frame.index:
                            analysis_frame.loc[i,'Allele_ID'] = self.extractAlleleID(gene, analysis_frame.loc[i,'Allele'])
                        analysis_frame.set_index('Allele_ID',inplace=True)
                        self.allele_data[gene] = analysis_frame
                        try:
                            analysis_frame.to_csv(os.path.join(backupDir,'Allele_info_{}.tab'.format(gene)),sep='\t')
                        except:
                            print("Warning: failed to save info about alleles")
                    except (IOError, KeyError):
                        self.allele_data[gene] = None
                        print("Failed to open allele file for gene {}; contact developer.".format(gene))
                        print(file)
        ##TODO: may need to check that all loci have a reference sequence
        print("Evaluating alleles for {} loci".format(sum(self.LocusFrame['allele_sequences'].notnull())))
        Peps = self.LocusFrame['isPeptide'] == True
        print("Treating {} sequences as peptides".format(sum(Peps)))
        ORFs = self.LocusFrame['isORF'] == True
        print("Treating {} genes as ORFs".format(sum(ORFs)))
        ORF_alleles = self.LocusFrame[ORFs].index
        print("Treating the following genes as ORFs: {}".format(', '.join(ORF_alleles)))
#         self.query_basenames = self.readAlleleRefNames(self.allele_reference_names_file)
        ##MLST profiles
        self.MLST_schemes = dict()
        if os.path.isfile(self.local_profile_file):
            refDir = os.path.dirname(self.local_profile_file)
            with open(self.local_profile_file) as profiles:
                for line in profiles:
                    values = line.split()
                    profile_file = os.path.join(refDir,values[1])
                    profile_name = values[0]
                    assert os.path.isfile(profile_file), "MLST scheme {} does not have a file: {}".format(profile_name,profile_file)
                    self.MLST_schemes[profile_name] = profile_file
        else:
            print("No local MLST profiles found")

    def getGenesWithPeptides(self):
        result = defaultdict(list)
        pep_frame = self.LocusFrame[self.LocusFrame['DNA_version'].notnull()]
        for _,row in pep_frame.iterrows():
            result[row['DNA_version']].append(row['locus'])
        return result
        
        
    def getMLSTschemes(self):
        return self.MLST_schemes.copy()
        
    def getAlleleRefFile(self,gene):
#         result = self.local_alleles[gene] if gene in self.local_alleles else None
#         return  result
        result = self.LocusFrame.loc[gene,'allele_sequences'] if gene in self.LocusFrame.index else None
        return result
    
    def getAllRefFiles(self):
        return self.LocusFrame['allele_sequences'].dropna().tolist()
        
    def getAlleleRefName(self,gene):
#         return self.query_basenames[gene]
        result = self.LocusFrame.loc[gene,'basename'] if gene in self.LocusFrame.index else None
        return result
    
    def getAlleleDataFrame(self,gene):
        result = self.allele_data[gene] if gene in self.allele_data else None
        return result
    
    def getLoci(self):
        return self.LocusFrame['locus'].tolist()
    
    
    def isORF(self,gene):
        return (gene in self.LocusFrame.index) and (self.LocusFrame.loc[gene,'isORF'] == True)
    
    def expected_gene(self,gene):
        return (gene in self.LocusFrame.index) and (self.LocusFrame.loc[gene,'expected'] == True)
    
    def isPep(self,gene):
        return (gene in self.LocusFrame.index) and (self.LocusFrame.loc[gene,'isPeptide'] == True)

import argparse
def main():
    ## Simple argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--version','-V',action='version',version='%(prog)s {}.{}'.format(script_version,script_subversion))
    parser.add_argument('-s','--setting_dir',help='Location of setting files')
    parser.add_argument('-r','--reference_dir',help='Location of reference files')
#     parser.add_argument('-o','--output_dir',help='Location to write any output')
    parser.add_argument('--update',help="Update files in reference dir")
    args = parser.parse_args()
    
    homeDir = os.path.dirname(os.path.realpath(__file__))
    settingDir = args.setting_dir if args.setting_dir else os.path.join(homeDir,'settings/')
    referenceDir = args.reference_dir if args.reference_dir else os.path.join(homeDir,referenceSubdirectory)
#     outputDir = args.output_dir if args.output_dir else os.getcwd()
    arm = AlleleReferenceManager(settingDir,referenceDir)   
    if args.update:
        arm.updateReferences(True) 
    
if __name__ == "__main__":
    main()
    
#     _arm.updateAllFiles()

########
# LocusExtractor
# Created by Adam Retchless for the Meningitis lab in the CDC, under contract with IHRC. Inc.
# Version 0.8, 20 Mar 2015
#
# The organization of this script is horrible. Sorry. - ACR

#pylint: disable=global-statement, broad-except
script_version = 1.5
script_subversion = 7 ##Added notes about composite coverage

import os
import sys
import re
import pandas as pd
import numpy as np
import utilities
import seq_utilities
import genomeOrganizer ##Note. This should be replaced with NGS_data_utilities at some point.
from BLASThelpers import BLASTheaders as bh
import BLASThelpers 
from SequenceExporter import SequenceExporter
import AmpliconExtractor
# import SRST2_controller
from AlleleReferenceManager import AlleleReferenceManager, referenceSubdirectory
from LookupTableManager import LookupTableManager
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq

from Bio.Blast.Applications import NcbiblastnCommandline, NcbitblastnCommandline
from Bio import SeqIO
from shlex import quote as sq
import shutil
import getpass
import time
import traceback


_debug = False

# import traceback
import warnings
# import sys

def warn_with_traceback(message, category, filename, lineno, file=None, line=None):
    print("Start Warning:")
    traceback.print_stack()
#     log = file if hasattr(file,'write') else sys.stderr
    print(warnings.formatwarning(message, category, filename, lineno, line))
    print("End warning.")

warnings.showwarning = warn_with_traceback

pep_messages = {
    'yes_locus': 'Peptide not found even though DNA locus was identified',
    'no_locus' : 'Peptide not found; locus not present',
    'stop' : '-AfterStopCodon',
    'out' : '-OutOfFrame'        
             }

notFound = 'Not found'

warn_edge = '-AtEdge'
warn_frameshift = '-Frameshift'
warn_insertion = '-Insertion'
warn_disruption = '-Disruption'

key_additional = 'Additional'
multiple = 'multiple'
    
def vprint(text):
    if _debug:
        print(text)


### Similarity requirement for identifying locus by imperfect match to known allele: don't want to hit homologs. I have no good way of setting this
####abcZ has two alleles in the reference file with < 75% identity

initial_table_columns = ['Filename','Unique_ID','Analysis_Version','Analysis_User','Analysis_Time','Lab_ID']

_min_identity = 0.7
_min_coverage = 0.8
_warning_distance_edge = 1000

## set format for BLAST tabular output
_BLASTheaderList = ['qseqid','sseqid','length','qcovhsp','qstart','qend','qlen','sstart','send','slen','qcovs',
                    'evalue','bitscore','pident','nident','mismatch','gapopen','gaps','qframe','sframe','sstrand','positive']
                    
# _outfmt_str = '\'{}\''.format(' '.join(['6']+_BLASTheaderList))
# _outfmt_head = [bh[h] for h in _BLASTheaderList]
_outfmt_str, _outfmt_head = BLASThelpers.BLASTtableCommandAndHeaders(_BLASTheaderList)

LE_version='%(prog)s {}.{}'.format(script_version,script_subversion)
### other global variables 
# _genes_to_query = set()


####Start organizing the files and reading in all the settings

class PrimaryExporter:
    MLST_headers = ['ST','clonal_complex']

    ##Setup export file; define header that are independent of the allele reference files
    headers = {}
    headers['ID'] = 'Lab_ID'
    headers['Nm_ST'] = 'Nm_MLST_ST'
    headers['Nm_clonal_complex'] = 'Nm_MLST_cc'
    headers['Hi_ST'] = 'Hi_MLST_ST'
    headers['PorA_type'] = 'PorA_type'    
        
    
    def __init__(self,parent,export_template_file,export_reference_file,lookupDir):
        ##TODO: these other variables can be drawn from the parent
        
        ##Location for writing output and intermediate files   
        
        
        self.reference_manager = parent.reference_manager ## the LocusExtractor object
        self.lookupDir = lookupDir
        #Get headers
        if os.path.isfile(export_template_file):
            self.export_template = pd.read_csv(export_template_file,header=0)
        else:
            raise IOError("Need to supply an export table file: {}".format(export_template_file))
        #Merge with list of files in genome_frame -- use filename as index (unique identifier)
        if parent.genomeFrame is not None:
            self.allele_table = parent.genomeFrame[initial_table_columns].copy()
#             self.export_table = pd.merge(self.allele_table,export_template,how='left') #inclusive of all columns and rows
        else:
            ##Record all alleles, separate from standardized output 
            self.allele_table = pd.DataFrame()
#             self.export_table = export_template
        #Map genes to headers
        if os.path.isfile(export_reference_file):
            with open(export_reference_file) as headers_in:
                for line in headers_in: #should be two items; tab delimited 
                    if not re.match(r'\s*#',line): #comment line
                        fields = line.split()
                        self.headers[fields[0]] = fields[1]
                        if len(fields) > 2:
                            print("Warning: A line in {} has more than two items in it: {}".format(export_reference_file,line))
        else:
            raise IOError("Need to supply a key linking genes to export table fields: {}".format(export_reference_file))
        #Confirm consistancy of headers and the reference file: There may be fields in the table that are not connected to anything
        for (value, header) in self.headers.items():
            if header not in self.export_template.columns:
                print("Warning: cannot find header for {}. Should be {}".format(value,header)) ## ToDo: guess at header and change to warning
        #MLST
        self.MLST_schemes = dict()
        

    
    def save_lookup(self,filename,text_dir):
        ##Make a dict of data frames -- one for each gene with lookup table.   Return them so they are accessible to the mol sheet
        ## Load lookup tables
        if os.path.isdir(self.lookupDir):
            lookupTables = LookupTableManager(self.lookupDir,set(self.reference_manager.getLoci()))
        ###Create blank tables
        lookup_tables_export = {x :  pd.DataFrame() for x in lookupTables.lookupGeneList()}
        ##Iterate over each genome
        for _, row in self.allele_table.iterrows():
            for gene in lookupTables.lookupGeneList():
                assert gene in lookup_tables_export, 'lookup tables and export must be synchronized'
            ##First, establish identifier
                export_series = pd.Series({'Filename':row['Filename'],'Unique_ID':row['Unique_ID'],'Lab_ID':row['Lab_ID']})
                allele = row[gene]
                export_series = export_series.append(lookupTables.lookupRow(gene,allele))
                lookup_tables_export[gene] = lookup_tables_export[gene].append(export_series,ignore_index=True)

        ##save to directory of csv
        csv_dir = os.path.join(text_dir,os.path.splitext(filename)[0])
        utilities.safeMakeDir(csv_dir)
        for gene, table in lookup_tables_export.items():
            csv_file = os.path.join(csv_dir,'{}_lookup.csv'.format(gene))
            try:
                utilities.safeOverwriteCSV(csv_file,table,index=False)
            except IOError:
                print("Failed to export lookup data to "+csv_file)
        ##save to multi-tab excel
        xlsx_file = utilities.setExt(filename,'.xlsx')
        try:
            writer = pd.ExcelWriter(xlsx_file)
            for gene, table in lookup_tables_export.items():
                table.to_excel(writer,gene,index=False)
            writer.save()
        except Exception as e:
            print("Unable to save Excel file {}. Use the CSV version. Warning: Excel will try to convert some values to dates unless you tell it not to during import.".format(filename))
            print(format(e))
            print("at line:")
            traceback.print_tb(sys.exc_info()[2])
            return lookup_tables_export
    
    ##This makes changes to the allele table that will not be saved if save_allele happens first
    def save_mol(self,filename,text_dir):
        
        ## Load lookup tables
        if os.path.isdir(self.lookupDir):
            lookupTables = LookupTableManager(self.lookupDir,set(self.reference_manager.getLoci()))
        ##Get some identifiers for writing to table
        ST_head = self.headers['Nm_ST']    
        CC_head = self.headers['Nm_clonal_complex']
        ###Create blank table
        export_table = pd.DataFrame()
        ##Iterate over each genome
        for i, row in self.allele_table.iterrows():
            try:
                ##First, establish identifier
                export_series = row[initial_table_columns].copy()
    #             export_series = pd.Series({'Filename':row['Filename'],'Unique_ID':row['Unique_ID'],'Lab_ID':row['Lab_ID']})
                ##Then transfer all the relevant genes, translating the header column
                for header, value in row.iteritems():
                    if header in self.headers:
                        export_series[self.headers[header]] = value
                ##Record MLST information
                ST_ID, CC_ID = self.findST('Nm',row)
                self.allele_table.loc[i,ST_head] = ST_ID
                if ST_ID.startswith('New'):
                    ST_ID = 'New'
                export_series.loc[ST_head] = ST_ID
                export_series.loc[CC_head] = CC_ID
                ##Record Hi MLST
                Hi_ST, _ = self.findST('Hi',row)
                self.allele_table.loc[i,'Hi_ST'] = Hi_ST
                if Hi_ST.startswith('New'):
                    Hi_ST = 'New'
                export_series.loc[self.headers['Hi_ST']] = Hi_ST
                ## Make PorA nomenclature
                PorA_ID = self.exportPorAType(row)
                export_series['PorA_type'] = PorA_ID
                ##Fill in antigen nomenclature from lookup table
                # simple transfers
                for gene in lookupTables.lookupGeneList():
                    allele = row[gene]
                    #For export table
                    for dest, source in lookupTables.transferHeaders(gene):
                        if pd.notnull(allele) and allele.isdigit():
                            value =  lookupTables.lookup(gene,allele,source)
                        else:
                            value = 'Allele not identified for {}. Cannot lookup {}'.format(gene,source)
                        export_series[dest] = value
    #                 #For the massive dump file
    #                 for header in lookupTables.transferRawData(gene):    
    #                     if header.lower().startswith(gene.lower()):
    #                         allele_header = header
    #                     else:
    #                         allele_header = gene + '_' + header
    #                     if pd.notnull(allele) and allele.isdigit():
    #                         value = lookupTables.lookup(gene,allele,header)
    #                         if value == '':
    #                             value = 'No lookup value'
    #                     else:
    #                         value = "Allele not identified"
    #                     self.allele_table.loc[idx,allele_header] = value
                                        
                #### Do validations and recodings for each gene sucessively 
                fHbp = 'fHbp'
                fHbp_allele = row[fHbp]
                try:
                    if str(fHbp_allele).isdigit():
                        ##Validation of peptide
                        pep_lookup = lookupTables.lookup(fHbp,fHbp_allele,'peptide_id')
                        if pep_lookup.startswith('no peptide_id value'):#blank ##See LookupTableManager.lookup
                            pep_lookup = lookupTables.lookup(fHbp,fHbp_allele,'flags')
                            if pep_lookup.startswith('no flags value'): ##See LookupTableManager.lookup
                                pep_lookup = 'no information'
                        if not isinstance(pep_lookup,str): ##This preceeds an exception
                            print("Error (not fatal): pep_lookup is a {} valued at {}".format(type(pep_lookup),pep_lookup))
                        FHbp = 'FHbp_pep'
                        pep_BLAST = row[FHbp]
                        if pd.isnull(pep_BLAST) or not pep_BLAST.isdigit():
                            if not pep_lookup.isdigit(): #Lookup table provided information that BLAST had no access to
                                pep_BLAST += ';' + pep_lookup
                                export_series[self.headers[FHbp]] = pep_BLAST
                                pep_lookup = pep_BLAST ##Just so the next step doesn't fail; already added lookup to BLAST               
                        if pep_lookup != pep_BLAST:
                            print("Warning: Conflicting fHbp peptide assignments...")
                            print("Sequence search: {}".format(pep_BLAST))
                            print("Allele lookup: {}".format(pep_lookup))
                            print("Lookup tables will be queried using the sequence search result")
                except AttributeError:
                    print(str(fHbp_allele))
                ## Add to table
                export_series.loc['NhbA_Protein_subvariant_Novartis'] = Nov_format(row['NhbA_pep'])
                ## nadA
                nadA_allele = row['nadA']
                NadA_pep = row['NadA_pep']
                Nov_nadA = 'Error. See alleles output for details. Contact developer.'
                if pd.notnull(NadA_pep) and NadA_pep.isdigit():
                    NadA_var = lookupTables.lookup('NadA_pep',NadA_pep,'NadA_variant')
                    if not (NadA_var.startswith('no ') or NadA_var.startswith('allele ')): ##See LookupTableManager.lookup
                        Nov_nadA = '{}.{}'.format(NadA_var,NadA_pep)
                    else:
                        Nov_nadA = 'peptide {}; family unknown'.format(NadA_pep)
                    if pd.notnull(nadA_allele) and nadA_allele.isdigit(): ##Just check for consistancy
                        NadA_pep_lookup = lookupTables.lookup('nadA',nadA_allele,'NadA_peptide')
                        if (NadA_pep_lookup.isdigit()) and (int(NadA_pep) != int(NadA_pep_lookup)):
                            print("Warning: Conflicting nadA peptide assignments...")
                            print("Sequence search: {}".format(NadA_pep))
                            print("Allele lookup: {}".format(NadA_pep_lookup))
                            print("Lookup tables will be queried using the peptide sequence search result, rather than the DNA allele")
                elif pd.notnull(nadA_allele) and nadA_allele.isdigit(): #This really should not happen
                    print("NadA peptide is not available for {}, but DNA allele is. The peptide variant value will be queried using the nucleotide sequence search result".format(row['Unique_ID']))
                    NadA_var = lookupTables.lookup('nadA',nadA_allele,'NadA_variant')
                    NadA_flag = lookupTables.lookup('nadA',nadA_allele,'flags')
                    if NadA_var.startswith('no '): ##See LookupTableManager.lookup
                        if not NadA_flag.startswith('no '): ##See LookupTableManager.lookup 
                            Nov_nadA = '{}'.format(NadA_flag)
                    else:
                        if NadA_flag.startswith('no '):##See LookupTableManager.lookup
                            Nov_nadA = '{}  (peptide ID unavailable)'.format(NadA_var)
                        else:
                            Nov_nadA = '{}  {}'.format(NadA_var,NadA_flag)
                elif NadA_pep in [pep_messages['yes_locus'],pep_messages['no_locus']]: ##Presence of DNA locus not really relevant, since there is often amplification of the deletion
                    Nov_nadA = notFound
                elif warn_edge in NadA_pep:
                    Nov_nadA = 'Incomplete ORF. Possible transposon insertion.'
                    ###TODO: see warn_edge source for how to provide more info
                elif pd.notnull(NadA_pep):
                    Nov_nadA = NadA_pep
                
                
                    
                        
                export_series.loc['NadA_Protein_subvariant_Novartis'] = Nov_nadA
#                 export_table = export_table.append(export_series,ignore_index=True)
            except Exception as e:
                print("Failed to format molecular data for {}".format(row['Unique_ID']))
                print(str(e))
                print("at line:")
                traceback.print_tb(sys.exc_info()[2])
            export_table = export_table.append(export_series,ignore_index=True)
        ##Add all columns from the template, and re-order according to template while avoiding any duplications
        export_table = export_table.append(self.export_template)
        export_table_headers = [x for x in initial_table_columns if x not in self.export_template.columns.tolist()] + self.export_template.columns.tolist()
        export_table = export_table[export_table_headers] 
        assert self.allele_table['Unique_ID'].tolist() == export_table['Unique_ID'].tolist(),"Export tables are out of order"
        csv_base = filename if not isinstance(text_dir,str) else os.path.join(text_dir,os.path.basename(filename))
        csv_file = utilities.setExt(csv_base,'.csv')
        utilities.safeOverwriteCSV(csv_file,export_table,index=False)
        xlsx_file = utilities.setExt(filename,'.xlsx')
        if not utilities.safeOverwriteTable(xlsx_file,export_table,'excel',index=False):
            print("Unable to save Excel file {}. Use the CSV version. Warning: Excel will try to convert some values to dates unless you tell it not to during import.".format(filename))
        json_file = utilities.setExt(filename,'.json')
        utilities.safeOverwriteTable(json_file,export_table,'json')
            
            

        
   
    def save_alleles(self,filename,column_order=None,text_dir=None):
        if column_order is None:
            column_order = []     
        new_column_order = [x for x in column_order if x in self.allele_table.columns]
        if len(new_column_order) != len(column_order):
            new_set = set(new_column_order)
            old_set = set(column_order)
            print("#################")
            print("Warning: allele data table is missing the following columns:")
            print("\t"+",".join(old_set.difference(new_set)))
        ### Report if any of the alleles have an internal stop codon
        for idx, row in self.allele_table.iterrows(): #for each genome
            stop_list = [] # record internal stops
            for item in row.index:#evaluate each gene,
                allele_frame = self.reference_manager.getAlleleDataFrame(item) #Returns None if not existant
                if allele_frame is not None:
                    allele_ID = row.loc[item]
                    if isinstance(allele_ID, str) and allele_ID.isdigit():
                        try:
                            if allele_frame.loc[allele_ID,'InternalStop']: # == 'True'
                                stop_list.append(item)
                        except KeyError:
                            print("Allele {} is not in lookup list. Contact developer.".format(allele_ID))
            self.allele_table.loc[idx,'InternalStopsInKnownAlleles'] = ','.join(stop_list) if len(stop_list) > 0 else 'No internal stops'
            
                                
        ### Need to be careful to do save_mol first since it updates the allele_table by adding information from lookup tables
        self.allele_table['nhbA_Novartis_format'] = self.allele_table['NhbA_pep'].apply(Nov_format)
        ## Arrange columns according to parameter -- any unspecified columns get sorted alphabetically
        cols = [x for x in initial_table_columns if x not in column_order] + [c.strip() for c in column_order if c in self.allele_table.columns]
        remainder = [c.strip() for c in self.allele_table.columns.tolist() if c not in cols]
        remainder.sort(key=lambda s: s.lower())
        cols += remainder
        try:
            if text_dir is None:
                csv_file = filename
            else:
                csv_file = os.path.join(text_dir,os.path.basename(filename))
            utilities.safeOverwriteCSV(csv_file,self.allele_table[cols],index=False)
        except IOError:
            print("Unable to save final allele table to CSV.")
        xlsx_file = utilities.setExt(filename,'.xlsx')
        try:
            utilities.safeOverwriteTable(xlsx_file,self.allele_table[cols],'excel',index=False)
        except IOError:
            print("Unable to save Excel file {}. Use the CSV version. Warning: Excel will try to convert some values to dates unless you tell it not to during import.".format(filename))

#     def save_temp_alleles(self,filename,column_order=None):
#         try:
#             utilities.safeOverwriteCSV(filename,self.allele_table[cols],index=False)
#         except IOError:
#             print("Unable to save temporary allele table to CSV.")
    #~ ##Designate an index for this isolate. The only unique idetifier is the filename itself
    #~ def establishIndex(filename):
        #~ 
        #~ 
    def loadMLSTscheme(self,Identifier,MLST_profile_file):
        assert os.path.isfile(MLST_profile_file)
        profile_table = pd.read_table(MLST_profile_file,header=0,dtype=str)
        cc_list = profile_table['clonal_complex'].unique()
        vprint("Loading profile table for {}. Has {} profiles in {} clonal complexes".format(Identifier,len(profile_table),len(cc_list)))

        MLST_genes = []
        locus_list = self.reference_manager.getLoci()
        for header in profile_table.columns:
            SpeciesLocus = '{}_{}'.format(Identifier,header)
            if (SpeciesLocus in locus_list) or (header in locus_list):
                MLST_genes.append(header)
            elif header not in self.MLST_headers:
                print("Notice: MLST header \"{}\" is not in the list of genes to search for.".format(header))
        this_scheme = dict()    
        this_scheme['genes'] = MLST_genes
        this_scheme['profile_table'] = profile_table
        self.MLST_schemes[Identifier] = this_scheme
        
    def exportAlleleID(self,genomeName,genomeFile, gene,allele_ID):
        if allele_ID is None:
            allele_ID = notFound
        self.addItemToAlleles(genomeName,genomeFile,gene,allele_ID)

    def addItemToAlleles(self,genomeName,genomeFile,header,value):
        i = self.getIndex(genomeName,genomeFile)
        self.allele_table.loc[i,header] = value
        
    def noteDuplicateRegion(self,genomeName,genomeFile,gene):
        dups = 'Duplicates'
        if dups not in self.allele_table:
            self.allele_table[dups] = ''
        i = self.getIndex(genomeName,genomeFile)
        n = self.allele_table.loc[i,dups]
        if isinstance(n,str) and len(n) > 0:
            n += ' {}'.format(gene)
        else:
            n = gene
        self.allele_table.loc[i,dups] = n
        
    ##Pass * to match all
    def getIndex(self,genomeName,genomeFile):
        at = self.allele_table
        if genomeName == '*':
            nameMatch = at['Unique_ID'] != ''
        else:
            nameMatch = at['Unique_ID'] == genomeName
        if genomeFile == '*':
            fileMatch = at['Filename'] != ''
        else:
            fileMatch = at['Filename'] == genomeFile
        match = at[ nameMatch & fileMatch]
        idx = match.index.tolist()
        if len(idx) != 1:
            print("Error finding genome: {}".format(genomeName))
            print("\tMatching names: {}".format(sum(nameMatch)))
            print("\tMatching files: {}".format(sum(fileMatch)))
            raise IOError("Failure to find index of genome")
        
        result = idx[0]
#         assert self.export_table.ix[result,'Lab_ID'] == genomeName, 'Genome name: {}'.format(genomeName)
#         assert self.export_table.ix[result,'Filename'] == genomeFile, 'Genome file: {}'.format(genomeFile)
        return result
        

    ## Finds ST if it is the profile table and genes have already been identified
    ## Identifier is species
    ## allele_series is the row of allele data
    ### New STs will be added to the profile table with the "uniqueID" from this batch.
    def findST(self,Identifier,allele_series):
        ##get index for genome
#         file_index = self.getIndex(genomeInfo['name'],genomeInfo['original'])
        this_scheme = self.MLST_schemes[Identifier]
        MLST_genes = this_scheme['genes']
        ## Filter profiles based on results for each gene
        profile_table = this_scheme['profile_table']
        profile_filtered = profile_table.copy()
        #Search for each locus
        thisST = {'clonal_complex':None} ##Failure to set this results in a spurious match between thisSt and table STs with no Clonal Complex. I don't know why
        ###TODO: figure out why omitting "clonal_complex" results in matches
        CC_ID = 'None identified'
        try:
            for gene in MLST_genes:
                SpeciesLocus = '{}_{}'.format(Identifier,gene) ##Need this because both Hi and Nm use the same gene name
                if SpeciesLocus in allele_series:
                    allele_ID = allele_series.loc[SpeciesLocus]
                elif gene in allele_series:
                    allele_ID = allele_series.loc[gene]
                else:
                    allele_ID = None
                    print("Error: MLST scheme for {} does not include locus {}".format(Identifier,gene))
                ##Narrow down potential profiles
                if isinstance(allele_ID,int):
                    filter_ID = str(allele_ID)
                elif isinstance(allele_ID,str):
                    if allele_ID.isdigit():
                        filter_ID = allele_ID
                    elif allele_ID == notFound:
                        filter_ID = '0'
                    elif allele_ID.startswith('New'):
                        filter_ID = '-1'
                    else:
                        raise ValueError('Illegal MLST allele: {}'.format(allele_ID))
                else:
                    raise ValueError('Illegal MLST allele: {}'.format(allele_ID))
    #             if not pd.isnull(allele_ID) and allele_ID not in ['New','Not found']:
    #                 filter_ID = str(allele_ID) 
    #             else:
    #                 filter_ID = '0'        # Value of 0 should eliminate all STs 
                ##Assure that there is no confusion from assigning "None" to 0
    #             if (filter_ID < 1 and allele_ID is not None):
    #                 print("Warning: Invalid allele value for gene {} in genome {}: {}".format(gene,genomeInfo['name'],allele_ID))
    #             profile_filtered = profile_filtered[profile_filtered[gene] == filter_ID]
                thisST[gene] = filter_ID
        except ValueError:
            ST_ID = 'Error: Illegal MLST allele'
        else:
            ##Check for valid ST
            result_set = set()
            for g in MLST_genes:
                result_set.add(thisST[g])
            null_set = set('0')
            if result_set == null_set:
                ST_ID = 'Not applicable'
            elif result_set > null_set:
                ST_ID = 'Error: Not all loci present'
            else:
                ST_ID = 'New'
            profile_filtered['matches'] = np.sum(profile_filtered == pd.Series(thisST),axis=1) # pylint: disable=no-member
            profile_filtered = profile_filtered.sort_values(by=['matches'],ascending=False)
            best_profile = profile_filtered.iloc[0]
            most_matches = best_profile['matches']
            profile_filtered = profile_filtered[profile_filtered['matches'] >= most_matches]
            count = len(profile_filtered.index)
            if most_matches == len(MLST_genes):
                ST_ID = best_profile.loc['ST']
                CC_ID = best_profile.loc['clonal_complex']
                if count > 1:
                    raise Exception("Corruption of MLST profile table -- multiple ST with same alleles")
            elif ST_ID == 'New': ##No match
                print('Unable to find {} MLST for {}. Best match is {} alleles'.format(Identifier,allele_series['Unique_ID'],most_matches))
                max_mismatch = 3
                max_in_list = 10
                mismatch = len(MLST_genes) - most_matches
                in_list = len(profile_filtered)
                if (mismatch <= max_mismatch) or (in_list < max_in_list):
                    for _, row in profile_filtered.iterrows():
                        try:
                            this_ST = row.loc['ST']
                            this_CC = row.loc['clonal_complex']
                        except Exception:
                            this_ST = None
                            this_CC = None
                        if pd.isnull(this_CC):
                            this_CC = 'unassigned'
                        print('\tClose match to {} ST {} from CC {}'.format(Identifier,this_ST,this_CC))
                else:
                    print("There are {} {} STs with {} mismatches. Not printing list".format(in_list,Identifier,mismatch))
                unique_CC = profile_filtered['clonal_complex'].unique()
                if most_matches >= len(MLST_genes) - max_mismatch:
                    unique_goodCC = [x for x in unique_CC if pd.notnull(x)] 
                    if len(unique_goodCC) == 1:
                        if pd.notnull(unique_goodCC[0]): ##TODO: find better way to deal with MLST schemes lacking clonal complexes
                            print('Single CC among best matches: {}'.format(unique_goodCC[0]))
                            #CC_ID = "Most similar to {} ({}/{} matches)".format(unique_goodCC[0],most_matches,len(MLST_genes))
                CC_ID = 'N/A'
                ##Record this ST in the table if all alleles are defined
                defined = True
                for gene in MLST_genes:
                    if not str(thisST[gene]).isdigit(): ##CC and ST are givn non-numeric values
                        defined = False
                if defined:
                    ST_ID = "New_ST-"+allele_series['Unique_ID']
                    thisST['ST'] = ST_ID
                    thisST['clonal_complex'] = CC_ID
                    this_scheme['profile_table'] = profile_table.append(thisST,ignore_index=True)
            elif ST_ID.startswith('Error'):
                print("Error identifying {} ST. Some loci are present, others absent".format(Identifier))
        return ST_ID, CC_ID
#         ST_head = self.headers['ST']    
#         CC_head = self.headers['clonal_complex']
#         self.export_table.loc[file_index,ST_head] = ST_ID
#         self.export_table.loc[file_index,CC_head] = CC_ID
        
    def exportPorAType(self,allele_series):
        PorA_ID = None
        if 'porA' in allele_series.index:
            #find index - allele_table and export_table share indicies
#             i = self.getIndex(genomeName,genomeFile)
            allele_ID = allele_series.loc['porA']
            ##Note: whether PorA is out of frame is not relevant for typing, but it is for vaccine interpretation
            ##TODO: confirm if this "is null" test is still relevant. 
            VR1_ID = allele_series.loc['PorA_VR1_pep']
            VR2_ID = allele_series.loc['PorA_VR2_pep']
            if (VR1_ID == notFound) or (VR2_ID == notFound) or VR1_ID.startswith('New') or VR2_ID.startswith('New'):
                if (allele_ID == notFound):
                    PorA_ID = notFound
                elif allele_ID.startswith('New'):
                    PorA_ID = 'New'
                    print("Need to extract variable regions from PorA allele")
                else:
                    PorA_ID = 'New'
                    print("Error: PorA allele was found in reference file but VR sequences were not. Contact developer.")
            elif (VR1_ID == VR2_ID) and VR1_ID in pep_messages.values():
                PorA_ID = VR1_ID ##This is only if both VRs are missing
            else:
                PorA_ID = "P1.{},{}".format(VR1_ID,VR2_ID)
        else:
            print("Error:PorA has not been analyzed. Notify developer")
        return PorA_ID
    
#Takes a string representation of an integer, and gives it the Novartis format for nhbA allels
def Nov_format(allele):
    if str(allele).isdigit():
        out = "p{:04}".format(int(allele))
    else:
        out = allele
    return out

def ConditionalInsert(pid,tempname):
    return utilities.appendToFilename(tempname, "_"+pid) if pid else tempname 

class LocusExtractor:
    def __init__(self,gd,args,ref_man,setting_dir,output_dir):
        self.outDir = output_dir
        self.textDir = os.path.join(self.outDir,'Results_text')
        utilities.safeMakeDir(self.textDir)
        self.settingDir = setting_dir
        
        self.blast_tempDir = os.path.join(self.outDir,'blast_temp_files/')## clean this up at the end
        utilities.safeMakeDir(self.blast_tempDir)
          
        self.DNA_dump_file = ConditionalInsert(args.projectID,os.path.join(self.outDir,'mismatched_DNA.fasta'))
        self.pep_dump_file = ConditionalInsert(args.projectID,os.path.join(self.outDir,'mismatched_peptides.fasta'))
        self.primary_export_file = ConditionalInsert(args.projectID,os.path.join(self.outDir,'molecular_data.csv'))
        self.lookup_export_file = ConditionalInsert(args.projectID,os.path.join(self.outDir,'lookup_data.csv'))
        self.allele_export_file = ConditionalInsert(args.projectID,os.path.join(self.outDir,'allele_data.csv'))
        self.sequence_export_file = ConditionalInsert(args.projectID,os.path.join(self.outDir,'sequence_data.csv'))
        self.blast_summary_file = ConditionalInsert(args.projectID,os.path.join(self.outDir,'blast_summaries.tab'))
        
        self.export_table_file = os.path.join(self.settingDir,'molecular_export_template.csv')
        self.export_reference_file = os.path.join(self.settingDir,"locus2molecular_export_headers.txt")
        self.export_sequences_file = os.path.join(self.settingDir,'sequence_export_template.csv')
        self.sequence_export_list = os.path.join(self.settingDir,"locus4sequence_export.txt")
        
        self.primer_file = os.path.join(self.settingDir,"locus2primers.csv")
        
        self.genomeFrame = gd
        self.genomeFrame['Analysis_Version'] = 'LocusExtractor.py {}.{}'.format(script_version,script_subversion)
        self.genomeFrame['Analysis_User'] = getpass.getuser()
        self.genomeFrame['Analysis_Time'] = time.ctime()#strftime("%c")
        self.reference_manager = ref_man
        
        self.export_best_match = args.export_best_match
        self.preserve_BLAST_hits = args.preserve_BLAST_hits
        
        
#         if args.is_reads:
#             print("Not implemented. Not planning on it...")
# # #             gd = convertPairedReadsToSingles(gd)
# #             for _,row in gd.iterrows():
# #                 queryOptions, _ = SRST2_controller.constructQueryOptions(row,self.outDir)
# #                 ref_list = self.reference_manager.getAllRefFiles()
# #                 full_command = SRST2_controller.constructFullCommand(queryOptions, ref_list)
# #                 SRST2_controller.run_SRST2(full_command)
# # #         gd = S RST2_controller.convertPairedReadsToSingles(readFrame)
#         else:
        self.loadSettings(args)
        for _,row in gd.iterrows():
            try:
                filename = row.loc['Filename']
                uniqueid = row.loc['Unique_ID']
            except KeyError:
                print("Error")
            else:
                if (not isinstance(filename,str)) or (not os.path.exists(filename)):
                    print("Error: cannot locate file for {}: {}".format(uniqueid,filename))
                else:
                    try:
                        (file_format,compressed) = utilities.guessFileFormat(filename)
                        self.evaluateGenome(uniqueid,filename,file_format,compressed)
                    except Exception as e:
                        print("Failed to evaluate genome file {}. Contact developer".format(filename))
                        print(format(e))
                        print("at line:")
                        traceback.print_tb(sys.exc_info()[2])
#                         if _debug:
#                             raise
                    try:
                        self.primary_exporter.allele_table.to_csv(os.path.join(self.outDir,'incremental_alleles.tab'),sep='\t')
                    except IOError:
                        print("Failed to save incremental allele table.")
        self.finish()
    
    def loadSettings(self,args):
        ##This is the main setting manager (reference files for alleles)
        print('## Begin Loading Settings ##')

        self.reference_manager.loadReferences(utilities.safeMakeOutputFolder(os.path.join(self.outDir,'References')))
        
        #Check some files    
        self.DNA_dump_file = utilities.checkForOverwrite(self.DNA_dump_file)
        self.pep_dump_file = utilities.checkForOverwrite(self.pep_dump_file)
    
        ## Load template file, bind alleles to fields, and load MLST information
        lookupDir = os.path.join(self.settingDir,'lookupTables/')
        self.primary_exporter = PrimaryExporter(self,self.export_table_file,self.export_reference_file,lookupDir)
        
        for identifier, filename in self.reference_manager.getMLSTschemes().items():
            assert os.path.isfile(filename), "MLST scheme {} does not have a file: {}".format(identifier,filename)
            self.primary_exporter.loadMLSTscheme(identifier,filename)
            
        ##Load the other export file template, along with gene bindings
        self.sequence_exporter = SequenceExporter(self.export_sequences_file,self.sequence_export_list,self.genomeFrame)
    
        ##Read in primer file
        self.amp_extractor = AmpliconExtractor.AmpliconExtractor(self.primer_file,working_dir=self.outDir,generate_output=self.preserve_BLAST_hits)
        self.blast_summary_frame = pd.DataFrame()
        
        print('## Finished Loading Settings ##')
        print('')



    #####Start  processing the genome
    
    
    #####Functions#######3
    
    ##Returns a Pandas Series object representing the allele with the best hit from BLAST
    #Gene: name
    #Query_file: FASTA file with named alleles of locus being searched for
    #genome_info: dict from AmpliconExtractor.setupGenomeForBlastBasedExtraction; includes 'db' for BLAST db to search against
    ##DNA searches try to do full length match of a similar, long sequence (i.e. megablast, with high reward for matches)
    ##Protein searches try to do exact match of short sequence (i.e. tblastn)
    
    ###Issue: this has no way to report multiple hits to the allele table. Should it return None? A list?
    def bestAlleleByBlast(self,gene,query_file,genome_info,is_DNA=True, is_subregion=False):
        if not isinstance(query_file,str) and not os.path.isfile(query_file):
            raise ValueError("Invalid query filename: {}".format(query_file))        
        db_name = genome_info['db']
        if not isinstance(db_name,str):
            raise ValueError("Invalid BLAST database name: {}".format(db_name))
        db_base = os.path.basename(db_name)
        (db_base,_) = os.path.splitext(db_base)
        outfile = os.path.join(self.blast_tempDir,gene+'.'+db_base+'.blast.txt')  
        if is_DNA:
            ##Try to force full-length alignment by increasing relative value of rewards
            blast_cline = NcbiblastnCommandline(query=sq(query_file),db=sq(db_name),outfmt=_outfmt_str,out=sq(outfile),evalue=0.1,reward=2,penalty=-2,gapopen=4,gapextend=2)
        else:
            blast_cline = NcbitblastnCommandline(query=sq(query_file),db=sq(db_name),outfmt=_outfmt_str,out=sq(outfile),evalue=0.1,window_size=15,matrix='BLOSUM80',seg='no')
            #A very strict matirx (PAM30) may be best...but I'm not seeing any performance problem even with default BLOSUM65. Seg was a major problem
        stdout = stderr = None
        try:
            stdout, stderr = blast_cline()
        except Exception as e:
            print("Blast failed on {} with {}...output below...".format(gene,query_file))
            print("\t{}".format(stdout))
            print("\t{}".format(stderr))
            print(format(e))
            print("at line:")
            traceback.print_tb(sys.exc_info()[2])
        results = pd.read_table(outfile,names=_outfmt_head)#No headers in file
        results['aligned_sites'] = results[bh['length']] - results[bh['gaps']]
        results['coverage'] =  results['aligned_sites'] / results[bh['qlen']]
        results['min_distance_to_edge'] = results[bh['sstart']].combine(results[bh['slen']]-results[bh['send']],min)
        #Clean up file
        if self.preserve_BLAST_hits:
            results.to_csv(outfile)
        else:
            os.remove(outfile)
        #Extract best hit
            ### Scenarios:
            # 1) perfect match: both coverage and pident are 100; others are less
            # 2) divergent sequence: prefer to have a full-length match rather than a perfect match to a subregion
            # 3) truncated sequence (assembly limitation): prefer perfect identity (with high coverage) over longer coverage
        ##Low identity is never valid (don't want to hit homolog). TODO: find a valid way of setting this cutoff        
        good_identity = results[bh['pident']] >= _min_identity  * 100
        results = results[good_identity].copy()   
        ##Search for perfect match first
        full_overlap = results['coverage'] == 1 #This captures gaps, above
        full_identity = results[bh['pident']] == 100 #This captures mismatches
        perfect_hits = results[full_overlap & full_identity].copy()     
        best = None
        if len(perfect_hits) > 0:
            best = perfect_hits.sort_values(by=['bit score',bh['pident']],ascending=False).iloc[0]
            ##Subregions don't have clearly defined edges, and could have repetative sections, making it hard to say if we have a mismatch to another variant
            if is_subregion: #Beginnings and ends are defined for full length genes
                betterScore = results[bh['bitscore']] > best[bh['bitscore']]
                fewMismatch =  (results[bh['qlen']] - results[bh['nident']]) <= 3
                noGaps = results[bh['gaps']] == 0
                high_score = results[ betterScore & fewMismatch & noGaps]
                if len(high_score) > 0:
    #                 if is_DNA:
                    higher_count = len(high_score.groupby(bh['qseqid']))
                    print("Warning: There are {} queries for {} with a higher bit-score than the identified perfect hit, no gaps, and no more than 3 mismatchs".format(higher_count,gene))
                    print(" the sequence may actually be a mutated version of these longer sequences")
            if len(perfect_hits) > 1:
                print("WARNING: {} known alleles for {}".format(len(perfect_hits),gene))
#                 best['Warning'] = 'MultiPerfect' ##This should only be flagged if these alleles are in different locations. 
    #                 else: ##Peptide
    #                     fewNegative =  (high_score[bh['qlen']] - high_score['positive']) <= 1
    #                     if sum(fewNegative) > 0:
    #                         print("Warning: There are {} queries for {} with a higher bit-score than the identified perfect hit, no gaps, no more than 3 mismatchs and 1 non-conservative substitution".format(gene))
    #                         print(" the sequence may actually be a mutated version of these longer sequences")
        else:
            ###Assumes BEST is None.
            #############TODO###############
            ## This gets complicated, particularly with transposon insertions (NadA). I would like to add the following:
            ## 1) Group by query (intact alleles), and try to sum the full query matched. This cannot be qcovs, because teh matches will likely be on different contigs
            ## 2) Once a fragmented gene has been identified, revisit the full list of hits and see if the alleles with transposons provide a longer hit to the same contigs
            ## 3) other stuff: be aware of if gene fragment is N-terminus (query position 1) 
            
            allele_frame = self.reference_manager.getAlleleDataFrame(gene) 
            ## Focusing on hits with high sequence identity to intact genes
            if allele_frame is not None: ##Only exists for full length ORFs
                intact_alleles = allele_frame['FullORF']
                intact_queries = results[bh['qseqid']].isin(allele_frame[intact_alleles]['Allele'])
                results = results[intact_queries]
            if len(results) == 0: 
                if self.reference_manager.expected_gene(gene):
                    print("\tFailed to identify any sequence with at least {} sequence identity for {} meaningful query sequences".format(_min_identity,gene))
            else:
                ### First look for overall good hits
                good_coverage = results['coverage'] >= _min_coverage ##coverage is aligned_sites/query_length
                if sum(good_coverage) > 0:
                    intact_blurb  = 'for intact ORFs ' if allele_frame is not None else ''
                    print('Notice: There is no perfect match for {}. Only evaluating hits {} with identity > {}'.format(gene,intact_blurb,_min_identity)) 
                    good_hits = results[good_coverage].copy()
                    contigs_with_goodCoverage = len(good_hits[bh['sseqid']].unique())
                    queries_with_goodCoverage = len(good_hits[bh['qseqid']].unique())
                    print("\tThere are {} queries mapping to {} contigs with coverage over {}".format(queries_with_goodCoverage,contigs_with_goodCoverage,_min_coverage))     
                    if allele_frame is not None: ##If this is an ORF,Give priority to ORFs that are full length matches to ORFs.
                        ##Already limited results to ORF hits
                        temp_best = None ##For debugging
                        full_overlap = good_hits['coverage'] == 1 #This captures gaps, above
                        if sum(full_overlap) > 0:
                            for n,g in good_hits[full_overlap].groupby([bh['sseqid'],bh['sstart'],bh['send']]):
                                my_seq = self.extractAllele(genome_info,n[0],n[1],n[2])
#                                 my_name = "{}_{}_{};{}:{}-{}".format(genomeInfo['name'],gene.replace('_','-'),'_'.join(similarityName),contig_name,start,stop)
                                seq_info = seq_utilities.ORF_info(my_seq)
                                if seq_info['FullORF']:
                                    temp_best = g.sort_values(by=['bit score',bh['pident']],ascending=False).iloc[0]
                                    if (best is None) or (abs(int(temp_best[bh['sstart']])-int(temp_best[bh['send']])) > abs(int(best[bh['sstart']])-int(best[bh['send']]))):
                                        best = temp_best ##longest ORF matching a reference ORF
                            if temp_best is None:
                                print("\tIdentified full length matches for novel {} sequence, but they are not ORFs".format(gene))
                            else:
                                print("\tIdentified full ORF for novel {} sequence".format(gene))
                        else:
                            print("\tNo full length matches for novel {} sequence.".format(gene))
                    if best is None: ##Default: currently not assigning based on ORF matching
                        best = good_hits.sort_values(by=['bit score',bh['pident']],ascending=False).iloc[0] ##This will favor longer queries even if they have poor matches
                    if contigs_with_goodCoverage > 1:
                        best['Warning'] = 'MultiLocations_{}Contigs'.format(contigs_with_goodCoverage)        
                    ##Note: it may be best for this to be unconditional (even with perfect matches).
                    bestQuery_hits = (results[bh['qseqid']] == best[bh['qseqid']]) & good_coverage
                    if sum(bestQuery_hits) > 1:
                        best['Warning'] = 'MultiLocations_{}Query'.format(sum(bestQuery_hits))   
                        try:
                            print(results[bestQuery_hits][[bh['qseqid'],'aligned_sites','coverage']])
                        except Exception as e:
                            utilities.printExceptionDetails(e)    
                if best is None:
                    if self.reference_manager.expected_gene(gene):
                        print('\tNo matches for {} with high identity (>{}) and good coverage (>{})' .format(gene,_min_identity,_min_coverage))
                ### Report suspiciously good hits; choose a "best" if one might be disrupted by assembly
                high_ident_hits = results[bh['pident']] >= 99
                if sum(high_ident_hits) > 0:
                    high_ident = results[high_ident_hits]
                    high_groups = high_ident.groupby(bh['qseqid'])
                    high_names = ["{} ({} hits; {} max cov)".format(name,len(group),group[bh['qcovs']].max()) for name,group in high_groups]
                    print('\tthere is a 99% identical match for a sections of the following {} query sequences'.format(gene))
                    print("\t\t"+'; '.join(high_names))
                    near_edge = (results['min_distance_to_edge'] < _warning_distance_edge) ##TODO: warning distance should depend on query length
                    perfect_near_edge = results[near_edge & high_ident_hits]
                    if len(perfect_near_edge) > 0:                    
                        print("\t\t There are {} contigs with partial hits >99% identical less than {} bp from edge...".format(len(perfect_near_edge.groupby(bh['sseqid'])),_warning_distance_edge))
                        if best is None:
                            print("\t\t{} partial identical hits. Returning the hit with the highest bit-score".format(len(perfect_near_edge.groupby(bh['sseqid']))))
                            best = results.sort_values(by=['bit score'],ascending=False).iloc[0] 
                    else:
                        print('\tNo candidate fragmented loci for {} (i.e. truncated gene due to bad assembly)'.format(gene))
                if best is not None:
                    if (best['coverage'] < 1) and (best['min_distance_to_edge'] < _warning_distance_edge):
                        print('\tNotice: The best hit for {} is truncated and maps to {}bp from the the end of contig {}'.format(gene,best['min_distance_to_edge'],best[bh['sseqid']]))   
                        best['truncated'] = True  ##Need to follow up by checking for amplicon and remove this if it is found (indicating that locus is intact.
                        try: ##See the big TODO note at the beginning of this section                        
#                             if best[bh['qcovs']].astype(int) >= _min_coverage: ##Tri to reassemble the contig
                            best_query = best[bh['qseqid']] 
                            query_hits = results[results[bh['qseqid']] == best_query]
#                             if sum(query_hits[bh['qstart']] == 1) > 0:
#                                 print("\tStart position found")    
                            print("\tQuery {} found in :".format(best_query))
                            covered_positions = set()
                            for _,row in query_hits.iterrows():
                                s_start = row[bh['sstart']]
                                s_end = row[bh['send']]
                                print("\t\t{} ({}-{})".format(row[bh['sseqid']],s_start,s_end))
                                if s_start < s_end:
                                    min_pos = s_start
                                    max_pos = s_end
                                else:
                                    max_pos = s_start
                                    min_pos = s_end
                                covered_positions.update(set(range(min_pos,max_pos+1)))
                            my_min = min(covered_positions)
                            my_max = max(covered_positions)
                            print("\tCovered {}/{} positions, ranging from {} to {}".format(len(covered_positions),best[bh['qlen']],my_min,my_max))
                        except Exception as e:
                            print(e)
                            print("at line:")
                            traceback.print_tb(sys.exc_info()[2])
                            
                            
                else:  #best is None
                    if not is_DNA:  #Look for frameshifts
                        possible_frameshifts = (results[bh['qcovs']] >= (_min_coverage * 100)) ##coverage per subject, rather than individual HSP
                        if sum(possible_frameshifts) > 1:
                            best = results[possible_frameshifts].sort_values(by=[bh['pident'],'bit score'],ascending=False).iloc[0] ##Favor exact matches over long matches
                            print("Experimental: Disrupted protein for {}.".format(gene))
                            best['disruption'] = True
                            ##TODO: figure out how to merge frame-shifted matches and distinguish them from insertions
                            ### TODO: sstrand is not reported for peptides. Derive from frame? Or from start and stop?
                            for name, group in results.groupby([bh['qseqid'],bh['sseqid'],bh['sstrand']]):
                                pass         
        ##Check for duplicates only if it found at least one good one
        if best is not None:
            try:
                full_overlap = results['coverage'] == 1 #This captures gaps, above
                complete = results[full_overlap].copy()
                if len(complete) > 0:
                    others = (complete[bh['sseqid']] != best[bh['sseqid']])
                    near = abs(complete[bh['sstart']].astype(int) - best[bh['sstart']].astype(int)) < 500
                    complete_other = complete[others | ~near]
                    if len(complete_other) > 0:
                        groups =  complete_other.groupby([bh['sseqid'],bh['sstart']])
                        locations = len(groups) ##This may tend to overcount the number of locations, since small differences in the start will show up as different sites
                        best[multiple] = str(locations + 1)
                        self.primary_exporter.noteDuplicateRegion(genome_info['name'],genome_info['original'],'{}({})'.format(gene,locations))
                        for _,g in groups:
                            g_full_identity = g[bh['pident']] == 100 #This captures mismatches
                            g_perfect_hits = g[g_full_identity]     
                            g_best = None
                            if len(g_perfect_hits) > 0:
                                g_best = g_perfect_hits.sort_values(by=['bit score',bh['pident']],ascending=False).iloc[0]
                                (g_id,_) = self.getAlleleFromQuery(g_best,query_file,self.reference_manager.getAlleleRefName(gene))
                                if key_additional in best.index: ##perfect match only; use "multiple" for general reporting of imperfect hits
                                    best[key_additional].append(g_id)
                                else:
                                    best[key_additional] = [g_id]
                        
            except Exception as e:
                print("exception")
                print(format(e))
                print("at line:")
                traceback.print_tb(sys.exc_info()[2])
                raise
            self.extractIDFromBLAST(gene,best)       ##field QueryID to series                              
        return best
    
    def extractIDFromBLAST(self,gene,bestHit):
        if bestHit is not None:
            bestHit['QueryID'] = self.reference_manager.extractAlleleID(gene,bestHit[bh['qseqid']])
        
    
    def reportBestBLASTAllele(self,bestAllele,gene,genomeInfo):
        ##TODO: add to _blast_summary_frame
        pass
    #Checks if allele is in query_file (based on BLAST result), and returns allele  (Bio.SeqRecord object) plus it's ID if so (an integer or None) 
    #BestHit: A pandas series object derived from the tabular BLAST results
    #Query_File: the allele query file given to BLAST
    #Query_basename: The root name used to identify alleles in the query_file (ignore this to identify allele numbers)
    def getAlleleFromQuery(self,bestHit,query_file,query_basename,exact=True):
        ###TODO: move some of this to AllleleReferenceManager function with same name.
        my_seq = None
        allele_ID = None
        if bestHit is not None:    
            #Test if any match is perfect
            bestIsFullLength = (bestHit.loc[bh['qcovhsp']] == 100)
            alleleInQuery = bestIsFullLength and bestHit['mismatches'] == 0 and bestHit['gap opens'] == 0
            if alleleInQuery or not exact: #pull allele from query file
                best_query = bestHit.loc['query id']
                with open(query_file) as query_handle: ##TODO extract this to outside of genome loop? Pass open query file?
                    query_seqs = SeqIO.to_dict(SeqIO.parse(query_handle, "fasta"))
                    best_seq = query_seqs[best_query]
                    try:
                        allele_ID = re.search(query_basename+'(.+)$',best_query).group(1)
                    except Exception as e:
                        print('Failure to identify {} in {}'.format(query_basename,best_query))
                        print(format(e))
                        print("at line:")
                        traceback.print_tb(sys.exc_info()[2])
                    my_seq = best_seq        
#             if 'Warning' in bestHit:
#                 allele_ID += '_'+bestHit['Warning']
#             if allele_ID is None:
#                 print(bestHit)
        else:
            print('\tWarning: no hit for {}'.format(query_file))
        return allele_ID,my_seq
    
    
    ##Returns AlleleID, contigID, and start and stop positions.
    # AlleleID is either None (cannot find gene) or New (assuming that we are here because it does not match a reference)
    # start and stop positions are BLAST (i.e. 1) indexed. Numbers can extend beyond range of contig (i.e. negative).
    #   if start is higher than stop, need the reverse strand
    ## Primer_dict contains results from AmpliconExtractor.map_primers_to_genome. Defines the range that should be sequenced (BLAST coordinate system, inclusive)
    #
    ## TODO return a list of coordinates in case there are two reasonable locations defined by this info?
    def combineBLASTandPrimers(self,blastHit,primer_dict,ORFquery,isPep=False):
        assert isinstance(primer_dict,dict) or primer_dict is None, 'primer_dict is type {}: contact developer'.format(type(primer_dict))
        assert isinstance(blastHit,pd.Series) or blastHit is None, 'blastHit is type {}: contact developer'.format(type(blastHit))
        blast_length_abbrev = 'aa' if isPep else 'bp'
        allele_ID = None
        contig = None
        start = None
        stop = None
        similarityName = ['error1','error2'] ##First part is succinct, rest is details
        ## CHeck if primers have any info
        pGood = primer_dict is not None and len(primer_dict) > 0 #Note: warnings regarding pGood should come from outside this routine
        usePrimers = pGood
        intactORF = False
        #Start with BLAST since it has orientation information
        bGood = blastHit is not None
        if bGood: 
            b_contig = blastHit.loc[bh['sseqid']]
            b_start = blastHit.loc[bh['sstart']]
            b_stop = blastHit.loc[bh['send']]
            is_plus = b_start < b_stop
            bestIsFullLength = (blastHit.loc[bh['qcovhsp']] == 100)
            if not bestIsFullLength:
                print('\tBLAST hit is not full length of query: {}%'.format(blastHit.loc[bh['qcovhsp']]))
            blastSimilarity = blastHit[bh['pident']]
            intactORF = bestIsFullLength and ORFquery
            usePrimers = pGood and not intactORF
            best_match = blastHit['QueryID']
            blastLength = blastHit[bh['length']]            
        ###Four scenarios:
        if usePrimers and bGood: ##Expect primers to border the sequence-matched region; go with primer sites
            for name,primer_sites in primer_dict.items():
                if allele_ID is None: ##Go through list of primer sites, until finding one that matches BLAST
                    p_contig = primer_sites['contig']
                    p_start = primer_sites['start']
                    p_stop = primer_sites['stop']
                    if p_contig == b_contig:
                        ##Evaulate beginning of gene
                        if is_plus:
                            b_low = b_start
                            b_high = b_stop
                        else:
                            b_low = b_stop
                            b_high = b_start
                        low_dist = p_start - b_low ##should be negative
                        low_valid = False
                        if low_dist > 0:
                            print("\tWarning: Primers map past the beginning of gene region. Relying on gene homology only.")
                        elif low_dist < -500:
                            print("\tWarning: Primers map {} bp away from beginning of gene region. Relying on gene homology only".format(low_dist))
                        else:
                            low_valid = True
                        ##Evaluate end of gene
                        high_dist = p_stop - b_high ##should be positive
                        high_valid = False
                        if high_dist < 0:
                            print("\tWarning: Primers map before the end of the gene region.  Relying on gene homology only.")
                        elif high_dist > 500: 
                            print("\tWarning: Prmiers map {} bp away from the end of the gene region. Relying on gene homology only.".format(high_dist))
                        else:
                            high_valid = True
                        if high_valid and low_valid:
                            allele_ID = 'New'
                            contig = p_contig #Already checked that b and p agree
                            if bestIsFullLength: ##Expand range to include flanking regions
                                start = b_start
                                stop = b_stop     
                                similarityName = ['BLAST_{}_{}{}(100%)_allele_{}'.format(blastSimilarity,blastLength,blast_length_abbrev,best_match),
                                                  'PCRconfirmed']
                            else:                      
                                if is_plus:
                                    start = p_start 
                                    stop = p_stop
                                else:
                                    start = p_stop
                                    stop = p_start
                                similarityName = ['PCR_{}bp'.format(abs(start-stop)),
                                                  'confirmedByBlast_{}_allele_{}'.format(blastSimilarity,best_match)]
                    else:
                        print("\tWarning: Primers and Sequence search identified different genomic regions. Cannot identify gene.")
            #end of loop over p_dict
            if allele_ID is None: # failed to match primers with blast hits ... go with BLAST hits
                usePrimers = False
        if bGood and not usePrimers:
            print("\tNotice: Identifying gene region by homolog search only.")
            allele_ID = 'New'
            contig = b_contig
            start = b_start
            stop = b_stop
            if bestIsFullLength:
                similarityName = ['BLASTonly_{}_{}{}(100%)_allele_{}'.format(blastSimilarity,blastLength,blast_length_abbrev,best_match),''] 
            else:##Expand range to include flanking regions
                print("Buffering locus position due to ambiguous BLAST hit")
                start_buffer = blastHit.loc[bh['qstart']] * 2 + 50 ##Double the gap, plus 50 to include primers
                stop_buffer = (blastHit.loc[bh['qlen']] - blastHit.loc[bh['length']])*2 + 50
                if is_plus:
                    start -= start_buffer
                    stop += stop_buffer
                else:
                    start += start_buffer
                    stop -= stop_buffer
                aln_pcnt = blastHit.loc[bh['qcovhsp']]
                similarityName = ['BLASTonly_{}_{}{}({}%)_allele_{}'.format(blastSimilarity,blastLength,blast_length_abbrev,aln_pcnt,best_match),
                                  'buffered']
            
        if usePrimers and not bGood:
            if len(primer_dict) == 1:
                print("\tNotice: Identifying gene region by flanking primers only.")
                name = list(primer_dict.keys())[0]
                primer_sites = primer_dict[name]
                
                contig = primer_sites['contig']
                start = primer_sites['start']
                stop = primer_sites['stop']
                allele_ID = 'New-PCR-{}bp'.format(abs(start-stop))
                similarityName = ['PCRonly','']
            else:
                print("\tNotice: Multiple potential sequencing sites for primers. Unable to choose one as correct...")
                print(primer_dict)
        if not pGood and not bGood: ##Neither good
            print('\tWarning: Failure to identify gene sequence or flanking primers')
        return allele_ID,contig,start,stop, intactORF, similarityName
      
                    
    ##extract allele from genome : returning Seq
    ## Start and stop are BLAST (i.e. 1) indexed. They may extend beyond range of contig. If start is higher than stop, need reverse strand
    def extractAllele(self,genomeInfo,contig,start,stop):
        is_for = start < stop
        if is_for:
            low = start
            high = stop
        else:
            low = stop
            high = start            
        temp_seq = genomeInfo['seqs'][contig].seq #Seq object
        if low < 1:
            low = 1
            print("\tWarning: attempting to extract a sequence that extends beyond the borders of contig {}".format(contig))
        if high > len(temp_seq):
            high = len(temp_seq)
            print("\tWarning: attempting to extract a sequence that extends beyond the borders of contig {}".format(contig))
        my_seq = temp_seq[low-1:high] ## Convert from BLAST indexing (1 indexed, inclusive of ends) to Python indexing (0 indexed; exclusive of high end)
        if not is_for:
            my_seq = my_seq.reverse_complement()
        return my_seq
    
    ##Save to DNA_sequence file, and returns a SeqRecord object
    ### my_seq must be either string or Bio.Seq object.
    def dumpAllele(self,my_seq,my_name):
        if not isinstance(my_seq,Seq) or not isinstance(my_name,str):
            print("Failed to write allele to output file")
        else:
            sr = SeqRecord(my_seq,id=my_name, name=my_name, description='')
            print("\tNew allele {} written to sequence dump file {}".format(sr.id,self.DNA_dump_file))
            with open(self.DNA_dump_file,"a") as fout:
                SeqIO.write(sr,fout,'fasta')
            return sr
        
    def dumpAlleleWithRef(self,my_seq,refence_blast,gene):
        assert isinstance(my_seq,SeqRecord)
        dumpDir = os.path.join(self.textDir,"AlleleWithRef")
        utilities.safeMakeDir(dumpDir)
        dumpFile = os.path.join(dumpDir,my_seq.name.split("_")[0]) + '_{}.fasta'.format(gene)
        query_file = self.reference_manager.getAlleleRefFile(gene)
        (allele_ID,allele_seq) = self.getAlleleFromQuery(refence_blast,query_file,self.reference_manager.getAlleleRefName(gene),exact=False)
        if (allele_ID is None) or (allele_seq is None):
                print("Failed to identify allele for {}...".format(gene))
                print("\t"+query_file)
                print("\t"+self.reference_manager.getAlleleRefName(gene))
                print(refence_blast)
#         sr = SeqRecord(allele_seq,id=str(allele_ID), name=str(allele_ID), description='')

        try:
            with open(dumpFile,"w") as fout:
                SeqIO.write(my_seq,fout,'fasta')
                SeqIO.write(allele_seq,fout,'fasta')
        except (TypeError, IOError) as e:
            print("Failed to export allele with reference: {}".format(my_seq.name))
            print(e)
        
    
    ##Find putative primer sequencing sites in genome
    # primerDict: master primer dictionary
    # gene: gene of interest
    # genomeInfo: data for this genome
    # region: subregion of gene to focus on
    # def getPrimerHits(amp_extractor,gene,genomeInfo,region='All'):
    #     primer_hit = None
    #     if gene in amp_extractor.primerDict.keys():
    # #         my_primer_dict = {gene:_primer_dict[gene]} #Ignore the other genes
    #         ##if we do not have sequencing primers for entire gene, use the PCR primers
    #         primer_file =  os.path.join(_blast_tempDir,gene+'.'+os.path.basename(genomeInfo['db'])+'.primers.txt') if _debug else ''
    #         primer_regions = amp_extractor.map_primers_to_genome(genomeInfo['db'],outfile=primer_file,search_set=set(gene),default_to_PCR=region=='All') ##locus/subregion/name:contig,start,stop
    #         primer_hit = primer_regions[gene][region] 
    #         if primer_hit is None:
    #             print("Notice: no primers for {}-{}".format(gene,region))
    #         elif len(primer_hit) == 0:
    #             print('Warning: primer binding sites cannot be identified for {}'.format(gene))
    #     return primer_hit
    
    ## Examines the information on the sequence of interest (BLASThit) and the sequencing primers (primer_hit) to extract gene sequence and save to DNA dumpfile
    ##Returns an allele_ID that includes information about the ORF (if available); an allele seq defined by the evidence (regardless of stop codons), and 
    ###   anda expectedORF which telss whether the sequence represents the region described as an ORF based on the BLASThit (pd.Series)
    #### If primer_hit is None, there was never a search for primer sites. If the search failed, len(primer_hit) == 0
    def getAlleleFromCombinedEvidence(self,BLASThit,primer_hit,genomeInfo,gene,isPep=False):
        allele_seq = allele_ID = None
        expectedORF = False
        if (BLASThit is not None) or (primer_hit is not None) or self.reference_manager.expected_gene(gene):
            (allele_ID,contig_name,start,stop,expectedORF,similarityName) = self.combineBLASTandPrimers(BLASThit,primer_hit,self.reference_manager.isORF(gene),isPep=isPep)##coordinates will be inverted if needed
            if allele_ID is not None: ##combineBLASTandPrimers identified a region for a new allele
                assert contig_name in genomeInfo['seqs'].keys(), "Contig key not valid : {}".format(contig_name)
                my_seq = self.extractAllele(genomeInfo,contig_name,start,stop) #Bio.Seq
                if not seq_utilities.unambiguous_sequence(my_seq):
                    allele_ID += '-AmbiguousCharacters'
                if expectedORF:
                    stop_codon = seq_utilities.find_first_stop(my_seq)
                    if not seq_utilities.internal_stop(my_seq,stop_codon):
                        allele_ID += "-ORF"
                    else:
                        allele_ID += "-InternalStop@{}".format(stop_codon)
                if BLASThit is not None:
                    if 'truncated' in BLASThit.index:
                        allele_ID += warn_edge ##
                    if 'disruption' in BLASThit.index:      
                        if 'frameshift' in BLASThit.index:
                            allele_ID += warn_frameshift
                        elif 'insertion' in BLASThit.index:
                            allele_ID += warn_insertion
                        else:
                            allele_ID += warn_disruption
                    if 'Warning' in BLASThit.index:
                        allele_ID += BLASThit['Warning']
                    blastLength = BLASThit[bh['length']]
                    if self.reference_manager.isPep(gene):
                        blastLength *= 3
                    allele_ID += '-'+similarityName[0]
                my_name = "{}_{}_{};{}:{}-{}".format(genomeInfo['name'],gene.replace('_','-'),'_'.join(similarityName),contig_name,start,stop)#remove underscore from gene name so it can be parsed out. Sigh.
                allele_seq = self.dumpAllele(my_seq,my_name) #Bio.SeqRecord
                if (BLASThit is not None) and self.export_best_match:
                    self.dumpAlleleWithRef(allele_seq, BLASThit, gene)
        return allele_ID,allele_seq,expectedORF

    
    
    
    
    ###Large routine for handling loci with specific peptide subregions of interest. ## TODO: incorporate this into the main program logic and use setting files to define these relationships
    ## Results are sent to the exporters and the sequence dump
    ### NOTE: these results are parsed by the exportPorA function. They need to be synchronized using the pep_messages dict
    def findAntigenSubregion(self,gene,subregions,genomeInfo,primer_regions):
        query_file = self.reference_manager.getAlleleRefFile(gene)
        if query_file is not None:
            best = self.bestAlleleByBlast(gene,query_file,genomeInfo) ##Caveat: I'm assuming there's only one locus in the genome...
            expectedORF = self.reference_manager.isORF(gene)
            self.reportBestBLASTAllele(best,gene,genomeInfo)
            if best is None:
                allele_ID = allele_seq = None
                if self.reference_manager.expected_gene(gene):
                    print('\tWarning: no hit for {}'.format(gene))
            else:
                (allele_ID,allele_seq) = self.getAlleleFromQuery(best,query_file,self.reference_manager.getAlleleRefName(gene))
            if (allele_ID is None): #Could not find a perfect match -- use primers, export to sequence dump file
                primer_hit = primer_regions[gene]['All'] if gene in primer_regions else None
                (allele_ID,allele_seq,expectedORF) = self.getAlleleFromCombinedEvidence(best,primer_hit,genomeInfo,gene)
            else:
                self.sequence_exporter.exportSequence(genomeInfo['name'],genomeInfo['original'],gene,allele_seq)
            self.primary_exporter.exportAlleleID(genomeInfo['name'],genomeInfo['original'],gene,allele_ID)
    
            if best is not None:
                if expectedORF:
                    locusBLAST,orf_seq = BLASThelpers.convertHitToORF(best,allele_seq,gene)
                else:
                    locusBLAST = best.copy()        
                    orf_seq = allele_seq
            else:
                locusBLAST = orf_seq = None
            #get subtypes
            for pep in subregions:
                pep_query = self.reference_manager.getAlleleRefFile(pep)
                bestPEP = self.bestAlleleByBlast(pep,pep_query,genomeInfo,False,True)
                self.reportBestBLASTAllele(bestPEP,pep,genomeInfo)
                if bestPEP is None:
                    if allele_seq is None: 
                        pep_ID = pep_messages['no_locus']
                    else:
                        pep_ID = pep_messages['yes_locus']
                else:
                    (pep_ID,_) = self.getAlleleFromQuery(bestPEP,pep_query,self.reference_manager.getAlleleRefName(pep)) #Note, this will return protein because of query file
                    if pep_ID is None:
                        primer_hit = primer_regions[gene][pep] if gene in primer_regions and pep in primer_regions[gene] else None
                        (pep_ID,pep_cds,_) = self.getAlleleFromCombinedEvidence(bestPEP,primer_hit,genomeInfo,pep,isPep=True)
                        if pep_cds is not None:#translate and save
                            if len(pep_cds) % 3 == 0:
                                pep_aa = SeqRecord(pep_cds.seq.translate(),id=pep_cds.id+'_translate',description='')
                                print("\tNew allele {} written to sequence dump file {}".format(pep_aa.id,self.pep_dump_file))
                                with open(self.pep_dump_file,"a") as fout:
                                    SeqIO.write(pep_aa,fout,'fasta')
                            else:
                                print("Error: Failure to extract {}. Length is {}".format(pep,len(pep_cds)))
                        else:
                            if allele_ID == 'New':
                                pep_ID = 'New'
                                allele_aa = SeqRecord(orf_seq.seq.translate(),id=allele_seq.id,description='')
                                print("\tNew allele {} written to sequence dump file {}".format(allele_aa.id,self.pep_dump_file))
                                with open(self.pep_dump_file,"a") as fout:
                                    SeqIO.write(allele_aa,fout,'fasta')
                                print("Need to extract variable regions from {} allele".format(gene))
                            elif allele_ID is not None:
                                pep_ID = 'New'
                                print("Error: {} allele was found in reference file but VR sequences were not. Contact developer.".format(gene))
                    if best is None:
                        print("Warning: Found peptide for {} in {} even though there was no DNA match.".format(gene,genomeInfo['name'])) 
                        pep_ID += '; DNA sequence not found'
                    else:                
                        if not BLASThelpers.hitContainsAnother(locusBLAST,bestPEP):  
                            if BLASThelpers.hitContainsAnother(best, bestPEP): ##not in trimed locus
                                pep_ID += pep_messages['stop']
                            else:                     
                                'Part of peptide {} identified outside of DNA locus'.format(pep_ID)
                            print("Warning: Peptide search for {} matches a region that is outside of locus defined by {}".format(pep,gene))
                        else:
                            start_site = abs(bestPEP[bh['sstart']] - locusBLAST[bh['sstart']])
                            if (start_site % 3) != 0:
                                pep_ID += pep_messages['out']                       
                self.primary_exporter.exportAlleleID(genomeInfo['name'],genomeInfo['original'],pep,pep_ID) 
        else:
            print("No query file for {}".format(gene))
    
    def evaluateWGS_reads(self,genome_name,read_file):
        print("## Begin searching read file {} ## ".format(genome_name))
    
        genes_with_peptides = self.reference_manager.getGenesWithPeptides()
        subregions_listed = []
        for _, region_list in genes_with_peptides.items():
            subregions_listed += region_list
        genes_to_query = dict()
        for gene in self.reference_manager.getLoci():
            if gene not in subregions_listed:
                query = self.reference_manager.getAlleleRefFile(gene)
                genes_to_query[gene] = query
#         for gene, query_file in genes_to_query.items():
#             pass
            ##TODO: condsider how/whether to handle antigen subregions
    #                 assert len(genomeInfo['seqs']) > 0, "No sequences parsed from file {}".format(genomeInfo['fasta'])
    #                 best = bestAlleleByBlast(gene,query_file,genomeInfo['db']) ##Caveat: I'm assuming there's only one locus in the genome...
    #                 reportBestBLASTAllele(best,gene,genomeInfo)
    #                 (allele_ID,allele_seq) = getAlleleFromQuery(best,query_file,_reference_manager.getAlleleRefName(gene))
    #                 if allele_ID is None: #Could not find a perfect match -- use primers, export to sequence dump file
    #                     ##merge blast and primers
    #                     primer_hit = primer_regions[gene]['All'] if gene in primer_regions.keys() else None#gene region
    #                     (allele_ID,allele_seq,_) = getAlleleFromCombinedEvidence(best,primer_hit,genomeInfo,gene)
    #                 else: 
    #                     if _reference_manager.isORF(gene):
    #                         first_stop = seq_utilities.find_first_stop(allele_seq)
    #                         if first_stop is not None and first_stop < len(allele_seq) - 3:
    #                             print("Notice: {} has an internal stop codon at position {}".format(gene,first_stop))
    #                         _sequence_exporter.exportSequence(genomeInfo['name'],genome_file,gene,allele_seq) ##only place perfect matches in this file
    #                 if allele_seq is None: 
    #                     print("no sequence found for {} in {}".format(gene,genomeInfo['name']))
    #                 self.primary_exporter.exportAlleleID(genomeInfo['name'],genome_file,gene,allele_ID)
        print('## Finished searching sequence {} ## \n'.format(genome_name))   
        
        
    def evaluateGenome(self,genome_name,genome_file,file_format = '',is_compressed = None):
        print("## Begin searching sequence {} ## ".format(genome_name))
        try:
            genomeInfo = AmpliconExtractor.setupGenomeForBlastBasedExtraction(genome_name,genome_file,self.blast_tempDir,file_format,is_compressed)
        except Exception as e:
            print("\nERROR!!!\nERROR!!! Unable to perform BLAST on {}. Make sure BLAST is available. Check you genome sequence then contact developer \n".format(genome_name))
            print(e)
#             if _debug:
#                 raise e
        else:
            #Search all primers # ToDo: use this dict instead of gene-specific searching
            primer_file =  os.path.join(self.blast_tempDir,os.path.basename(genomeInfo['db'])+'.primers.txt') if _debug else '' ##in this case, primer file is the place to write primer mappnig results to, so it will only be saved if "debug"
            primer_regions = self.amp_extractor.map_primers_to_genome(genomeInfo['db'],primer_file,default_to_PCR=True) ##locus/subregion/name:contig,start,stop
            ## nadA PCR is it's own thing
            nadA = 'nadA'
            nadA_PCR = 'None'
            if nadA in primer_regions:
                nadA_Amplicon = primer_regions['nadA']['OuterRange']
                if len(nadA_Amplicon) == 1:
                    PCR_range = nadA_Amplicon[0] #An AmpliconExtractor.RegionRecord
                    nadA_PCR = '{}bp'.format(abs(PCR_range.get_max()-PCR_range.get_min()))
                elif len(nadA_Amplicon) > 1:
                    nadA_PCR = 'multiple sites'
            self.primary_exporter.exportAlleleID(genomeInfo['name'],genome_file,'nadA_PCR',nadA_PCR)
            genes_with_peptides = self.reference_manager.getGenesWithPeptides()
            ##Handle peptides
            assert len(genomeInfo['seqs']) > 0, "No sequences parsed from file {}".format(genomeInfo['fasta'])
            #Search for remainder
            subregions_listed = []
            for _, region_list in genes_with_peptides.items():
                subregions_listed += region_list
            genes_to_query = dict()
            for gene in self.reference_manager.getLoci():
                if gene not in subregions_listed:
                    query = self.reference_manager.getAlleleRefFile(gene)
                    genes_to_query[gene] = query
            for gene, query_file in genes_to_query.items():
                try:
                    if gene in genes_with_peptides:
                        self.findAntigenSubregion(gene,genes_with_peptides[gene],genomeInfo,primer_regions)
                    else:
                        if query_file is None:
                            print("Unable to search for {} due to absence of query file".format(gene))
                            if _debug:
                                print("Try turning off debug/no_update mode")
                            else:
                                print("Check that the settings file has the proper URL. Contact developer")
                        else:
                            assert len(genomeInfo['seqs']) > 0, "No sequences parsed from file {}".format(genomeInfo['fasta'])
                            best = self.bestAlleleByBlast(gene,query_file,genomeInfo) ##Caveat: dulpicate hits reported to alleles data
                            self.reportBestBLASTAllele(best,gene,genomeInfo)
                            if best is None:
                                allele_ID = allele_seq = None
                                if self.reference_manager.expected_gene(gene):
                                    print('\tWarning: no hit for {}'.format(gene))
                            else:                
                                (allele_ID,allele_seq) = self.getAlleleFromQuery(best,query_file,self.reference_manager.getAlleleRefName(gene))
    #                             if key_additional in best.index: ##This should only occur if "multiple" is set, but I have not been too rigorous about this one
    #                                 additionals = best[key_additional] ##Only perfect hits right now
                                if multiple in best.index:
                                    allele_ID = 'Multiple ({}) loci'.format(best[multiple])                            
                            if allele_ID is None: #Could not find a perfect match -- use primers, export to sequence dump file
                                ##merge blast and primers
                                primer_hit = primer_regions[gene]['All'] if gene in primer_regions.keys() else None#gene region
                                (allele_ID,allele_seq,_) = self.getAlleleFromCombinedEvidence(best,primer_hit,genomeInfo,gene)
                            else: 
                                if self.reference_manager.isORF(gene):
                                    if allele_seq is not None:
                                        first_stop = seq_utilities.find_first_stop(allele_seq)
                                        if first_stop is not None and first_stop < len(allele_seq) - 3:
                                            print("Notice: {} has an internal stop codon at position {}".format(gene,first_stop))
                                        self.sequence_exporter.exportSequence(genomeInfo['name'],genome_file,gene,allele_seq) ##only place perfect matches in this file
                            if allele_seq is None: 
                                if self.reference_manager.expected_gene(gene):
                                    print("no sequence found for {} in {}".format(gene,genomeInfo['name']))
                            self.primary_exporter.exportAlleleID(genomeInfo['name'],genome_file,gene,allele_ID)
                except Exception as e:
                    print("Exception evaluating gene {}".format(gene))
                    utilities.printExceptionDetails(e) 
            print('## Finished searching sequence {} ## \n'.format(genome_name))   
    
    
    def finish(self):
        #Save final results
        print('## Begin exporting results ##')
        try:
            self.primary_exporter.save_lookup(self.lookup_export_file,self.textDir)
        except Exception as e:
            print("Failed to save lookup data: "+str(e))
        try:
            self.primary_exporter.save_mol(self.primary_export_file,self.textDir)  ## This updates the allele table...
        except Exception as e:
            print('Failed to save molecular data: '+ str(e)) 
        try: 
            self.primary_exporter.save_alleles(self.allele_export_file,self.reference_manager.getLoci(),self.textDir)
        except Exception as e:
            print('Failed to save allele data: '+ str(e)) 
        try:
            self.sequence_exporter.save(self.sequence_export_file)
        except Exception as e:
            print('Failed to save sequence data: '+ str(e)) 
        try:
            if len(self.blast_summary_frame) > 0:
                self.blast_summary_frame.to_csv(self.blast_summary_file,sep='\t')
        except Exception as e:
            print('Failed to save BLAST data: '+ str(e)) 
        # Cleanup
#         if not _debug: 
        shutil.rmtree(self.blast_tempDir)
        self.amp_extractor.finish()
        print('## Finish exporting results ##')
    
    
import argparse
def main():
    ##Default Settings
    homeDir = os.path.dirname(os.path.realpath(__file__))
    settingDir = os.path.join(homeDir,'settings/')
    referenceDir = os.path.join(homeDir,referenceSubdirectory)
    logFile = "LocusExtractor.log"
    
    old_argv = sys.argv.copy() ##For documentation
    parser = argparse.ArgumentParser(description='A program to identify and report specific sequences in genomes.',)
    parser.add_argument('--version','-V',action='version',version='%(prog)s {}.{}'.format(script_version,script_subversion))
    parser.add_argument('-p','--projectID',help='Provide an identifier that will be added to output directory and data table')
    parser.add_argument('-s','--setting_dir',help='Location of setting files')
    parser.add_argument('-m','--min_cov',help='Alternate minimum coverage',default=0.8,type=float)
    
#     parser.add_argument('-o','--organism',help='Limits search to specified organism. Default is to test for all sequences in setting file. Try "Hi" or "Nm"')
    parser.add_argument('--debug',action='store_true',help="Do not update reference files. Same as 'no_update'")
    parser.add_argument('--no_update',action='store_true',help="Do not update reference files. Same as 'debug'")
    parser.add_argument('--shallow_search_assemblies',help='Do not search subdirectories for assemblies',action='store_true')
    parser.add_argument('--export_best_match',action='store_true',help='Export files comparing new alleles to their best match.')
    parser.add_argument('--preserve_BLAST_hits',action='store_true',help='Keep raw BLAST result files')
#     parser.add_argument('--is_reads',action='store_true',help="Not implemented yet. Analyze the data as reads (default is to analyze an assembly)")
    parser.add_argument('args', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    argv = [os.path.basename(__file__)] + args.args  
    if len(argv) <= 1:
        sys.exit("No data files provided") 
        
    if args.setting_dir:
        settingDir = args.setting_dir
    global _debug     
    _debug = True if (args.debug | args.no_update) else False
    global _min_coverage ##TODO: do this properly (pass argument or something. Maybe put it in the locus list file to make it specific
    if args.min_cov:
        _min_coverage = args.min_cov
     
    ##Basic setup
    if args.projectID:
        outputBase = "LE"+'_{}.{}_{}'.format(script_version,script_subversion,args.projectID)
        logFile = utilities.appendToFilename(logFile, args.projectID)
    else:
        outputBase = "LocusExtractor"+'_v{}.{}'.format(script_version,script_subversion)
        
    outputDir = utilities.safeMakeOutputFolder(outputBase)
    sys.stdout = utilities.Logger(os.path.join(outputDir,logFile))
    
    ##Startup message
    print('############################')
    print(' Starting Locus Extractor')
    print()
    ###Deprecation warning
    import platform
    print("Using python version: {}".format(platform.python_version()))
    print("\tFound at {}".format(sys.executable))    
#     print('Notice: You are using Python pandas version {}'.format(pd.version.short_version))#pd._version.get_versions()['version']))
    pd.show_versions()   
#     pd.version 
    print(' ###### Command #######')
    print(' '.join(old_argv))
    print()
    print('Results will be found here: '+os.path.abspath(outputDir))

       
    
    ## Put the genomes into  a dataframe -- this will evaluate whether arguments are legit
    GO_settings = os.path.join(settingDir,genomeOrganizer.SETTING_FILE)
    try:   
        repo = genomeOrganizer.get_default_settings(GO_settings)['repository'] 
    except:
        repo = None
        print("Warning: failed to load repository indicated by "+GO_settings)
            
#     if args.is_reads:
#         gd = genomeOrganizer.placeReadsIntoDataFrame(argv,repository=repo)
#         ##TODO: Need to split the paired "reads" into separate "filenames"     
#     else:
    deep_search = not args.shallow_search_assemblies
    gd = genomeOrganizer.placeAssembliesIntoDataFrame(argv,repository=repo,deep_search=deep_search) 
    

        
    ## Run
    if gd is not None and len(gd) > 0: 
        ## Establish reference sequences
        reference_manager = AlleleReferenceManager(settingDir,referenceDir)
        ### Grab reference files (ToDo: make this a condintional process; do it only when necessary; abort slow downloads more quickly?)
        reference_manager.updateReferences(True,EssentialOnly = _debug)         
        utilities.safeOverwriteTable(genomeOrganizer.default_list(outputDir), gd, 'tab',index=False)
        LocusExtractor(gd,args,reference_manager,settingDir,outputDir)  
        print('Results will be found here: '+os.path.abspath(outputDir))
    else:
        print("No genome identified")


    

# from sys import argv
if __name__ == "__main__":
    if not utilities.has_preferred_python():
        raise Exception("Upgrade your python version")
    has_BLAST = BLASThelpers.test_executables()
    if has_BLAST is not None:
        sys.exit(has_BLAST)
    main()

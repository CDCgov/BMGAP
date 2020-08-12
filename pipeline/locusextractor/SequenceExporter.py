##Creates the sequence export sheet #just a utility for LocusExtractor


import pandas as pd
import re
import utilities
from seq_utilities import trim_at_first_stop

class SequenceExporter:
    def __init__(self,templateFile,locusList,genome_frame):
        #Read in teh template 
        templateFrame = pd.read_csv(templateFile,header=0)
         #Figure out what genes are in template, and what output is needed for each
        self.data_legend = dict()
        for header in templateFrame.columns:
            if header != "Lab_ID":
                #Gene and the output format
                (gene, dtype) = header.split('_',1)
                gene = gene.lower()
                if gene not in self.data_legend.keys():
                    self.data_legend[gene] = set()
                self.data_legend[gene].add(dtype)
        #Combine the columns with the list of files being tested
        self.data = pd.merge(genome_frame,templateFrame,how='left')
        #Doublecheck by using the locusList file. Not essential...but for safety
        self.gene_list = []
        with open(locusList) as locus_in:
            for line in locus_in:
                if not re.match('\s*#',line): #comment line
                    self.gene_list.append(line.strip().lower())
                    if self.gene_list[-1] not in self.data_legend.keys():
                        print('Notice: gene {} is in sequence export list but not in template'.format(self.gene_list[-1]))
        for gene in self.data_legend.keys():
            if gene not in self.gene_list + ['lab']:  #'lab' derives from "Lab_ID', but it was split at the underscore and then made lowercase
                print('Notice: gene {} is in sequence export template but not in list to export'.format(gene))
            
    def save(self,filename):
        utilities.safeOverwriteTable(filename,self.data,'csv')
            
    ##Allele_SeqRecord is a Bio.SeqRecord object
    #genomeName and gene are strings that are used for export keys and header lookup keys (in data_legend), respectively
    def exportSequence(self,genomeName,genomeFile,gene,allele_seqRecord):
        st = self.data ##sequence table abbreviation 
        nameMatch = st['Unique_ID'] == genomeName
        fileMatch = st['Filename'] == genomeFile
        bothMatch = nameMatch & fileMatch
        match = st[bothMatch]
        idx = match.index.tolist()
        if len(idx) == 1:
            i = idx[0]
            lgene = gene.lower()
            if lgene in self.gene_list and lgene in self.data_legend.keys():
                allele_seq = allele_seqRecord.seq
                self.data.loc[genomeName,'Unique_ID'] = genomeName
                data_set = self.data_legend[gene.lower()]
                key = 'DNA sequence'
                if key in data_set:
                    header = gene + '_' + key #extract this to method if it needs to be modified
                    for col in self.data.columns:
                        headerMatch = re.match(header,col,re.IGNORECASE)
                        if headerMatch:
                            self.data.loc[genomeName,col] = str(allele_seq)
                            break
                key = 'DNA sequence_length' 
                if key in data_set:
                    header = gene + '_' + key
                    for col in self.data.columns:
                        headerMatch = re.match(header,col,re.IGNORECASE)
                        if headerMatch:
                            self.data.loc[genomeName,col] = len(allele_seq)
                            break
                key = 'protein sequence' 
                if key in data_set:
                    header = gene + '_' + key
                    for col in self.data.columns:
                        headerMatch = re.match(header,col,re.IGNORECASE)
                        if headerMatch:
                            self.data.loc[genomeName,col] = str(trim_at_first_stop(allele_seq).translate())
                            break
    #                 print("Warning: failed to identify column with header: {}".format(header))
                key = 'protein sequence_length'
                if key in data_set:
                    header = gene + '_' + key
                    for col in self.data.columns:
                        headerMatch = re.match(header,col,re.IGNORECASE)
                        if headerMatch:
                            self.data.loc[genomeName,col] = len(trim_at_first_stop(allele_seq).translate())
                            break    
#                 print("Warning: failed to identify column with header: {}".format(header))
        else:
            raise IOError("Failed to identify index in sequence table")
                

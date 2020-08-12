import os
# import re
import pandas as pd
# import urllib.request

##This handles the lookup tables that are used to provide standard nomenclature for export. MLST profiles are still in the AlleleReferencManager, but should
## probably be moved to this object since they have a similar format and are used at a similar point in the proceses

class LookupTableManager:
    defaultLookupColumns= ['locus','allele_id','sequence','sequence length','comments']
    
    def __init__(self,_lookupDir,key_set = None):        
        ##Location of settings
        self.lookupTableDir = _lookupDir
        assert os.path.isdir(_lookupDir), 'Lookup directory does not exist; contact developer \n {}'.format(_lookupDir)
        self.tableKey = os.path.join(_lookupDir,'locus2lookup.tab')
        with open(self.tableKey,'rt') as fin:
            rows = [line.strip() for line in fin if line]
        rows = [row.split('\t') for row in rows if row] #strip blank lines
        assert len(rows) > 0, 'Lookup directory has invalid key file; contact developer'
        try:
            self.refDict = {row[0]:pd.read_table(os.path.join(_lookupDir,row[1]),index_col='allele_id',dtype=str) for row in rows}
        except Exception as e:
            print("Warning: failure to open lookup tables. Unable to get standard nomenclature for some genes. Contact developer")
            print("Exception "+ str(e))
        ## get keys for header conversion
        lookup2allele_file = os.path.join(_lookupDir,'lookup2allele.tab')
        self.lookup2allele = pd.read_table(lookup2allele_file,comment='#',dtype=str)
        self.lookup2allele.dropna(how='all',inplace=True)
        lookup2export_file = os.path.join(_lookupDir,'locus2lookup2export.tab')
        self.lookup2export = pd.read_table(lookup2export_file,comment='#',dtype=str)
        self.lookup2export.dropna(how='all',inplace=True)
        self.lookup2export.fillna('Not assigned',inplace=True)
        ### Validate keys
        if key_set is not None:
            primary_set = set(self.refDict.keys())
            allele_set = set(self.lookup2allele['locus'].tolist())
#             print(allele_set)
            export_set = set(self.lookup2export['locus'].tolist())
#             print(export_set)
            if not primary_set.issubset(key_set):
                print("Error: a locus in {} is not found in the main set of loci. Contact developer".format(self.tableKey))
            if not allele_set.issubset(key_set):
                print("Error: a locus in {} is not found in the main set of loci. Contact developer".format(lookup2allele_file))
            if not export_set.issubset(key_set):
                print("Error: a locus in {} is not found in the main set of loci. Contact developer".format(lookup2export_file))
            
    def lookup(self,gene,allele,header):
        table = self.refDict[gene]
        assert header in table.columns, "Invalid header {} in lookup table for {}".format(header,gene)
        if int(allele) in table.index:
            value = table.loc[int(allele),header]
        else:
            value = 'allele {} not in lookup table for {}'.format(allele,gene) 
            print('Warning: Invalid index value {} in lookup table for {}'.format(allele,gene))
            print("\t Lookup tables may need to be updated. See instructions in "+self.lookupTableDir)
            print("Or ask the data manager to handle this in the SQL database.")
        if (value is None) or (value == ''): ##Empty field in table
            value = 'no {} value for allele {} in {} table'.format(header,allele,gene)
        return value
    
    def lookupRow(self,gene,allele):
        table = self.refDict[gene]
        if pd.notnull(allele) and allele.isdigit() and (int(allele) in table.index):
            export_row = table.loc[int(allele)]
        else:
            export_row = pd.Series(data={x:None for x in self.defaultLookupColumns})                
            export_row['locus'] = table['locus'].tolist()[0]  ##Should all be the same
            export_row['allele_id'] =  str(allele)
            if pd.isnull(allele):
                export_row['comments'] = 'Locus not found'
            elif allele.isdigit():
                print('Warning: Invalid index value {} in lookup table for {}'.format(allele,gene))
                print("\t Lookup tables may need to be updated. See instructions in "+self.lookupTableDir)
                print("Or ask the data manager to handle this in the SQL database.")
                export_row['comments'] = 'Allele not in lookup table'
            else:
                export_row['comments'] = 'Allele not assigned an identifier'
        return export_row        
        
    
    def transferHeaders(self,gene):
        table = self.lookup2export
        frame = table[table['locus'] == gene]
        for _, row in frame.iterrows():
            dest = row['export'].strip()
            source = row['lookup'].strip()
            yield dest, source
        
    def transferRawData(self,gene):
        table = self.lookup2allele
        frame = table[table['locus'] == gene]
        for idx, row in frame.iterrows():
            header = row['header'].strip()
            yield header
    
    def lookupGeneList(self):
        return self.refDict.keys()
        
# import os
# import pandas as pd
# from collections import defaultdict
import numpy as np
import os
import utilities
import pandas as pd

SCRIPT_VERSION = 1 #Updatinng "listReadsWithFilename" to handle shallow shearch and report realpath
SCRIPT_SUBVERSION =  1# Remove filesizeZero column   

script_base = os.path.basename(__file__)
_outputBase = '{}_v{}.{}'.format(os.path.splitext(script_base)[0],SCRIPT_VERSION,SCRIPT_SUBVERSION)


capsuleGroups = {
 'A': ['csaA','csaB','csaC','csaD'],
 'B': ['csb'],
 'C': ['csc'],
 'W': ['csw'],
 'X': ['csxA','csxB','csxC'],
 'Y': ['csy']    
    }

capsuleGenes = [x for (sg,genes) in capsuleGroups.items() for x in genes]

def hasGenes(series,gene_list):
    gene_series = series[gene_list]
    if (gene_series == 'Not found').all():
        result = 'No' 
    elif (gene_series.str.match('\d+')).all():
        result = 'Yes'
    else:
        result = 'Maybe'
    return result

def geneParse(gene_str):
    parts = gene_str.split('_')
    print(parts)
    if parts[0] != 'New-ORF-BLAST':
        return 'unknown'
    else:
        return parts[1]
    
def isfloat(prospect):
    try:
        float(prospect)
    except:
        return False
    else:
        return True
    
##Modifies the allele frame that is passed    
def tag_cap_gene_presence(AF_copy):
    for SG,genes in capsuleGroups.items():
        AF_copy[SG] = AF_copy.apply(hasGenes,gene_list=genes,axis=1)
    AF_copy['SG_count'] = np.sum(AF_copy[[x for x in capsuleGroups.keys()]] == 'Yes',axis=1)
    AF_copy['SG_maybe'] = np.sum(AF_copy[[x for x in capsuleGroups.keys()]] == 'Maybe',axis=1)
    
    ###Modifies the allele frame pthat is passed
    ##Need to tag_cap_gene_presence first
def compareWY(AF_copy):
    for i in AF_copy.index:
        W = AF_copy.loc[i,'W']
        Y = AF_copy.loc[i,'Y']
        if W != 'No' and Y != 'No':
            print('index/ID = {}/{}'.format(i,AF_copy.loc[i,'Lab_ID']))
            if W == 'Yes' and Y == 'Yes':
                print('Both are yes. WTF?')
            elif W == 'Yes':
                assert Y == 'Maybe'
                AF_copy.loc[i,'Y'] = 'No'
                print('corrected Y')
            elif Y == 'Yes':
                assert W == 'Maybe'
                AF_copy.loc[i,'W'] = 'No'
                print('Corrected W')
            else:
                assert W == 'Maybe' and Y == 'Maybe'
                W_pcnt = geneParse(AF_copy.loc[i,'csw'])
                Y_pcnt = geneParse(AF_copy.loc[i,'csy'])
                W_float = isfloat(W_pcnt)
                if W_float:
                    W_val = float(W_pcnt)
                Y_float = isfloat(Y_pcnt)
                if Y_float:
                    Y_val = float(Y_pcnt)
                if W_float or Y_float:
                    if W_float and Y_float:                  
                        if W_val > Y_val:
                            AF_copy.loc[i,'Y'] = 'No'
                            print('corrected Y')
                        elif Y_val > W_val:
                            AF_copy.loc[i,'W'] = 'No'
                            print('Corrected W')
                        else:
                            assert Y_val == W_val
                            print("W and Y are equal!!!")
                    elif W_float:
                        assert not Y_float
                        AF_copy.loc[i,'Y'] = 'No'
                        print('corrected Y')
                    else:
                        assert Y_float
                        AF_copy.loc[i,'W'] = 'No'
                        print('Corrected W')
                else:
                    print('unable to judge')    
                    AF_copy.loc[i,'SG gene'] = 'Trunc XY'
    AF_copy['SG_count'] = np.sum(AF_copy[[x for x in capsuleGroups.keys()]] == 'Yes',axis=1)
    AF_copy['SG_maybe'] = np.sum(AF_copy[[x for x in capsuleGroups.keys()]] == 'Maybe',axis=1)
    
##Updates allelel frame
def accountForNewAlleles(allele_frame):
    for i,row in allele_frame[allele_frame.SG_count == 0].iterrows():
        if row['SG_maybe'] == 1:
            for SG, genes in capsuleGroups.items():
                if row[SG] == 'Maybe':
                    print("index/ID: {}/{}".format(i,row['Lab_ID']))
                    result = 'Yes'
                    for g in genes:
                        print(g)
                        hit = geneParse(row[g]) 
                        if not isfloat(hit):
                            if not row[g].isdigit():
                                result = 'Maybe'
                                print('No hit on {}: {}'.format(g,row[g]))
                    allele_frame.loc[i,SG] = result
                    if result == 'Yes':
                        print("Good one")   
    allele_frame['SG_count'] = np.sum(allele_frame[[x for x in capsuleGroups.keys()]] == 'Yes',axis=1)
    allele_frame['SG_maybe'] = np.sum(allele_frame[[x for x in capsuleGroups.keys()]] == 'Maybe',axis=1)
    
import argparse
      
def main():
#     epi_text = ('If no NGS data directory is given, will automatically scan the following directories recursively: \n' +
#                 '\tread directory: {}'.format(default_read_dir) +
#                 '\n\tassembly directory: {}'.format(default_ass_dir)+
#                 '\n\tMiSeq directory: {}'.format(default_BML_reads))
#,epilog=epi_text

    parser = argparse.ArgumentParser(description='A program call capsule types')
    ### general info
    parser.add_argument('--version','-V',action='version',version='%(prog)s {}.{}'.format(SCRIPT_VERSION,SCRIPT_SUBVERSION))
#     parser.add_argument('--debug',action='store_true',help="Preserve intermediate files and do not update reference files")

    ### controls

    ### required
#     parser.add_argument('--assembly_dir','-ad',help='Directory with assemblies')
#     parser.add_argument('--read_dir','-rd',help='Directory with reads')
#     parser.add_argument('--out_dir','-od',help='Output directory')   
    parser.add_argument('allele_table',help='LocusExtractor allele data table as input (excel format)')
#     parser.add_argument('')   
    args = parser.parse_args()
#     out_dir = args.out_dir if args.out_dir else utilities.safeMakeOutputFolder(_outputBase)
    allele_table = args.allele_table
    if os.path.isfile(allele_table):
        b = os.path.basename(allele_table)
        out = utilities.appendToFilename(b, 'withCapsuleCalls')
        af = pd.read_excel(allele_table)
        tag_cap_gene_presence(af)
        compareWY(af)
        accountForNewAlleles(af)
        af.to_excel(out,index=False)      
        ##TODO: this works pretty well, but:
        ## headers may not be clear (do I need to prefix with "capsule genes"?
        ## New_ORF is not identified as a likely active gene
        ## "SG gene" is only used for XY -- should it report other genes?
        ## Need to create a method to update the allele frame in place.
                
    else:
        print("No input file")
        


        
        

    
    
if __name__ == "__main__":
    if not utilities.has_preferred_python():
        raise Exception("Upgrade your python version")
    main()     
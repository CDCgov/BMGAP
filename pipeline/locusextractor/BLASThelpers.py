from subprocess import call, DEVNULL
import seq_utilities
import pandas as pd
import glob
# import shlex

version = 1.0 #Aug 2015

BLASTheaders = {
'qseqid': 'query id',
'qgi': 'query gi',
'qacc': 'query acc.',
'qaccver': 'query acc.ver',
'qlen': 'query length',
'sseqid': 'subject id',
'sallseqid': 'subject ids',
'sgi': 'subject gi',
'sallgi': 'subject gis',
'sacc': 'subject acc.',
'saccver': 'subject acc.ver',##may be depricated
'sallacc': 'subject accs.',
'slen': 'subject length',#may be deprecated 
'qstart': 'q. start',
'qend': 'q. end',
'sstart': 's. start',
'send': 's. end',
'qseq': 'query seq',
'sseq': 'subject seq',
'evalue': 'evalue',
'bitscore': 'bit score',
'score': 'score',
'length': 'alignment length',
'pident': '% identity',
'nident': 'identical',
'mismatch': 'mismatches',
'positive': 'positives',
'gapopen': 'gap opens',
'gaps': 'gaps',
'ppos': '% positives',
'frames': 'query/sbjct frames',
'qframe': 'query frame',
'sframe': 'sbjct frame',
'btop': 'BTOP',
'staxids': 'subject tax ids',
'sscinames': 'subject sci names',
'scomnames': 'subject com names',
'sblastnames': 'subject blast names',
'sskingdoms': 'subject super kingdoms',
'stitle': 'subject title',
'salltitles': 'subject titles',
'sstrand': 'subject strand',
'qcovs': '% query coverage per subject',
'qcovhsp': '% query coverage per hsp',
'qcovus' : '% query coverage without doublecounting subject positions'
}



# blast_dbs = {
# 'nr':'/blast/db/nr'
#              }
bh = BLASTheaders

blast_default_output = ['qseqid','sseqid','pident','length','mismatch','gapopen',
'qstart','qend','sstart','send','evalue','bitscore']

##Provides the command to get table-formatted BLAST output (no headers) along with the header column name
def BLASTtableCommandAndHeaders(BLASTheaderList):
    #command = '{}'.format(' '.join(['6']+BLASTheaderList)) # Reagan Had to modify this for it to work on BMGAP, but it broke my usage on BioLinux
    command = '\'{}\''.format(' '.join(['6']+BLASTheaderList))
    headers = [bh[h] for h in BLASTheaderList]
    return command, headers

blast_default_command,blast_default_headers = BLASTtableCommandAndHeaders(blast_default_output)


def loadBLASTtableToDataFrame(result_file,headers=blast_default_headers):
    return pd.read_table(result_file,names=headers)#No headers in file

def blankBLASTtable(headers=blast_default_headers):
    return pd.DataFrame(columns=headers)

    ##Compare two Pandas.Series objects originating from BLAST results
# Returns TRue if first in inside of second 
def hitContainsAnother(external,internal):
#     assert external is not None, "Don't check for range of BLAST it if there is no hit!"
    if (internal is None) or (external is None):
        return False
    e_start = external[bh['sstart']]
    e_end = external[bh['send']]
    if e_start < e_end:
        e_low = e_start
        e_high = e_end
    else:
        e_low = e_end
        e_high = e_start
    i_start = internal[bh['sstart']]
    i_end = internal[bh['send']]
    return (e_low <= i_start) and (e_low <= i_end) and (e_high >= i_start) and (e_high >= i_end)

## Takes a Pandas Series representing a BLAST hit (with s. start and s. end) and the sequence representing that region...
### Return a copy of the BLAST hit where it only contains an ORF (with no  stop codon)
def convertHitToORF(BLASThit,seq,identifier=''):
    newBlast = BLASThit.copy()
    stop = seq_utilities.find_first_stop(seq)
    if stop is not None:
        s_end = newBlast[bh['send']]
        s_start = newBlast[bh['sstart']]
        if s_end > s_start:
            newBlast[bh['send']] = s_start + stop - 1
        else:
            newBlast[bh['send']] = s_start - stop + 1
        if identifier and (len(seq) - stop > 3):
            print('\tTrimming {} ORF at internal stop: from {} to {} base pairs.'.format(identifier,len(seq),stop))
    return newBlast,seq[:stop]

def makeblastdb(genome_file,db_name=None):
    ### make search database for genome. Note: this will fail if genome_file or db_name have weird characters in it (space, parentheses). THere is no point in fixing it here because the problem will pop up elsewhere 
#     import os
#     print(os.environ["PATH"])
#     mkdb = r'makeblastdb -in {} -dbtype nucl -out {}'.format(shlex.quote(genome_file),shlex.quote(db_name))

    ##I cannot figure out if it is beter to use shlex.quote or not. I seem to have trouble either way and I cannot discern the rules
    if db_name is not None:
        mkdb = r'makeblastdb -in {} -dbtype nucl -out {}'.format(genome_file,db_name)
    else:
        mkdb = r'makeblastdb -in {} -dbtype nucl '.format(genome_file)
    if call(mkdb.split(),stdout=DEVNULL) != 0:
        raise Exception("Failure to produce BLAST database. Command was \n {}".format(mkdb))
    
    ##Currently only checks that there are files with appropriate roots
def checkblastdb(db_name):##confirm that database exists
    if not isinstance(db_name,str):
        raise TypeError('Database name must be string. It is {}'.format(type(db_name)))
    return len(glob.glob(db_name+'.*')) > 0

from shutil import which
#Returns none when everything is ok. Otherwise returns error message.
def test_executables():
    result = None
    if which('makeblastdb') is None:
        result = False
        result = "Cannot call makeblastdb. Confirm that BLAST is on the path."
    return result


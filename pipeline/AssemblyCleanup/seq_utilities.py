import Bio 
from Bio import SeqIO, Seq, SeqRecord
import re
import utilities
from Bio.Alphabet import IUPAC
import pandas as pd
from collections import defaultdict
import os
# from Collections import Sequence/
# import collections.Sequence
unambig = IUPAC.IUPACUnambiguousDNA.letters
unambig_set = set(unambig)
ambig_all_set = set(IUPAC.IUPACAmbiguousDNA.letters)
ambig_only_set = ambig_all_set.difference(unambig_set)

base_sets = {
    "DNA4": set([i.lower() for i in unambig_set] + [i.upper() for i in unambig_set]),
    "DNA4_upper": unambig_set,
    "DNA_ambig":set([i.lower() for i in ambig_all_set] + [i.upper() for i in ambig_all_set]),
    "Gaps":set('-')
}
# import pandas as pd
# from BLASThelpers import BLASTheaders as bh
script_version = 1.1 #27 Jan 2016

##Seq is a SeqRecord, Seq, or string
### Result is "None" or a location on the string (alt: should "none" be len(seq)?)
def convertToString(seq):
    s = seq
    if isinstance(s,Bio.SeqRecord.SeqRecord):
        s=s.seq
    if isinstance(s,Bio.Seq.Seq):
        s=str(s)
    return s
    
def find_first_stop(seq):
    s = convertToString(seq)
    if not isinstance(s, str):
        print("###Error###")
        print(seq)
        raise "Must have a string!"

    first = None
    for i in range(0,len(s),3):
        x=s[i:i+3]
        if x in ('TAA','TAG','TGA'):
            first = i
            break
    return first

##Seq is a SeqRecord, Seq, or string        
def trim_at_first_stop(seq):
    stop = find_first_stop(seq)
    if stop is None:
        return seq
    else:
        return seq[:stop]
    
def internal_stop(my_seq,stop_codon=None):
    if stop_codon is None:
        stop_codon = find_first_stop(my_seq)
    return (stop_codon is not None) and (stop_codon < len(my_seq) - 3)    
        
##Returns a list of dicts containing results from analyzing each gene
def ORF_analysis(multifasta):
    data = []
    with open(multifasta,'rt') as fin:
        for seq in SeqIO.parse(fin,'fasta'):
            seq_info = {'Allele':seq.name}
            seq_info['Length'] = len(seq)
            first_stop = find_first_stop(seq)
            seq_info['FirstStop'] = first_stop
            seq_info['InternalStop'] = internal_stop(seq,first_stop)
            data.append(seq_info)
    return data
            
def unambiguous_sequence(seq):
    s = convertToString(seq)
    safe_char = base_sets['DNA4']
    seq_set = set(s)
    return seq_set <= safe_char
    
# def has_internal_stop(seq):
#     return find_first_stop <


##Trims all bases from edges of "FASTQ_seq" until reaching first base with Qual score <= "qual"
def trimFASTQtoFirstBase(FASTQ_seq, qual):
    start = 0
    quals =  FASTQ_seq.letter_annotations["phred_quality"]
    while quals[start] < qual:
        start += 1
        if start == len(FASTQ_seq):
            return None 
    stop = len(FASTQ_seq)
    while quals[stop-1] < qual:
        stop -= 1 #No need to test for over-run, since we already found a stop point when looking from left
    return FASTQ_seq[start:stop]
    
def standardize_contig_names(contig_list,base_ID):
    new_contigs = []
    name_set = set([None])
    c = 0 #counter for un-named contigs
    for contig in contig_list:
        name_match = re.search(r'(\d+)$',contig.id) ##Search for digits
        ctgID = int(name_match.group(1)) if name_match else None
        while ctgID in name_set:
            c += 1
            ctgID = c
        name_set.add(ctgID)
        contig.id = '{}_ctg_{:03d}'.format(base_ID,ctgID)
        #~ contig.name = new_name
        #~ contig.description = '' ##Keep the original name as "description". This should be harmless for processing, but provide some context for users
        new_contigs.append(contig)
    return new_contigs, c    

def seq_guess_and_read(filename):
    seq = None
    seq_format, compressed = utilities.guessFileFormat(filename)
    if seq_format is not None:
        with utilities.flexible_handle(filename, compressed, 'rt') as seq_in:
            seq = SeqIO.read(seq_in,seq_format)
    else:
        print("Cannot infer sequence format for file: " + filename)            
    return seq

def seq_guess_and_write(seqs,filename):
    seq_format, compressed = utilities.guessFileFormat(filename)
    if seq_format is not None:
        with utilities.flexible_handle(filename, compressed, 'wt') as seq_out:
            SeqIO.write(seqs,seq_out,seq_format)
    else:
        print("Cannot infer sequence format for file: " + filename)              

# def seqs_guess_and_parse(filename):
#     seq = None
#     seq_format, compressed = utilities.guessFileFormat(filename)
#     if seq_format is not None:
#         with utilities.flexible_handle(filename, compressed, 'rt') as seq_in:
#             return SeqIO.parse(seq_in,seq_format)
#     else:
#         print("Cannot infer sequence format for file: " + filename)
#     return seq

def seqs_guess_and_parse2list(filename):
    seq = None
    seq_format, compressed = utilities.guessFileFormat(filename)
    if seq_format is not None:
        with utilities.flexible_handle(filename, compressed, 'rt') as seq_in:
            seq = [x for x in SeqIO.parse(seq_in,seq_format)]
    else:
        print("Cannot infer sequence format for file: " + filename)
    return seq

##will throw an IOError if bad filename
def seqs_guess_and_parse2dict(filename):
    if not isinstance(filename,str):
        raise TypeError("Filename must be string, is {}".format(type(filename)))
#     if not os.path.isfile(filename):
#         raise ValueError("Cannot locate file: {}".format(filename))
    seq_dict = None
    seq_format, compressed = utilities.guessFileFormat(filename)
    if seq_format is not None:
        with utilities.flexible_handle(filename, compressed, 'rt') as seq_in:
            seq_dict = SeqIO.to_dict(SeqIO.parse(seq_in,seq_format))
    else:
        print("Cannot infer sequence format for file: " + filename)        
    return seq_dict

##Note: as of now, these are all numbers.
def describeSequences(sequenceFile):
    result = defaultdict(int)
    result['FileSize'] = os.path.getsize(sequenceFile)
    seq_format, compressed = utilities.guessFileFormat(sequenceFile) ##guess and parse
    if seq_format is not None:
        with utilities.flexible_handle(sequenceFile, compressed, 'rt') as seq_in:
            for s in SeqIO.parse(seq_in,seq_format):
                result['Sequences'] += 1
                result['Nucleotides'] += len(s)        
    else:
        print("Cannot infer sequence format for file: " + sequenceFile)    
    ##TODO: add Q30 and such?
    return result


##Extract regions from seq, as defined by start and stop values in the tuples of region_list.
## If stop < start, extracted regions will be reverse complement of Seq
## Assume that values are indexed at 1, but allow them to be indexed at 0
def extractRegions(seq,region_list,basename='Region',index=1): ##Untested: Dec 19 2016
#     if not isinstance(region_table,pd.DataFrame):
#         raise TypeError("Region table should be a DataFrame, but is {}".format(type(region_table)))
    ##Validation
    if isinstance(seq,SeqRecord): ##Reduce sequence to string
        s = str(seq.seq)
    elif isinstance(seq,Seq):
        s = str(seq)
    elif isinstance(seq,str):
        s = seq
    else:
        raise TypeError("seq variable should be string, Seq, or SeqRecord, but is {}".format(type(seq)))
    if not isinstance(region_list,list):
        raise TypeError("Region list should be a list, but is {}".format(type(region_list)))
    for r in region_list: 
        r[0] -= index
        r[1] -= index
        if not isinstance(r,list):
            raise TypeError("Items in regions list should be list. Is {}".format(type(r)))##This should tolerate tuples too...
        if not (len(r) == 2):
            raise ValueError("Items in region list should be of length 2. Is {}".format(len(r)))
        if (r[0] >= len(s)) or (r[0] < 0):
            raise ValueError("Sequence indexes must be smaller than sequence length: {} and {}".format(r[0],len(s)))
        if (r[1] >= len(s)) or (r[1] < 1):
            raise ValueError("Sequence indexes must be smaller than sequence length: {} and {}".format(r[1],len(s)))
    if not isinstance(basename,str):
        raise TypeError('Basename must be string. is {}'.format(type(basename)))
    ##Extract
    seqs = []
    for r in region_list:
        beg = r[0]
        end = r[1]
        seq_name = '{}_{}_{}'.format(basename,beg,end)
        if beg < end:
            first = beg
            last = end
            Forward = True
        else:
            first = beg
            last = end
            Forward = False
        region = Seq.Seq(s[first,last+1])
        if not Forward:
            region = region.reverse_complement()
        sr = SeqRecord.SeqRecord(region,id=seq_name, name=seq_name, description='')
        seqs.append(sr) 
    return seqs

def describeShortSeqs(query_fasta):
    query_seqs = SeqIO.to_dict(SeqIO.parse(query_fasta,'fasta'))
    seqs_table = []
    for n,s in query_seqs.items():
        series = pd.Series()
        series['seq id'] = n
        series['seq length'] = len(s)
        char_count = defaultdict(int)
        for c in s.seq:
            char_count[c] += 1
        ambig_char = 0
        for c in char_count.keys():
            if c not in unambig_set:
                ambig_char += char_count[c]
        series['seq ambig'] = ambig_char
        series['seq ambig%'] = ambig_char/len(s) * 100
        seqs_table.append(series)
    seqs_frame = pd.DataFrame(seqs_table)    
    seqs_frame['seq unambig'] = seqs_frame['seq length'] - seqs_frame['seq ambig']
    seqs_frame['seq unambig%'] = seqs_frame['seq unambig']/seqs_frame['seq length'] * 100    
    return seqs_frame

     
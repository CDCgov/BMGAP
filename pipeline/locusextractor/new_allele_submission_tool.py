from Bio import SeqIO
# import sys
# sys.path.append('/scicomp/home/ymw8/ML/tools/Utility/')
# sys.path.append('/scicomp/home/ymw8/ML/tools/LocusExtractor')
import utilities
from collections import defaultdict
import argparse
script_version = 0.1
script_subversion = 2

def main():
    parser = argparse.ArgumentParser(description='A program to identify unique alleles for submission to PubMLST. Default behavior is to count the occurances of distinct sequences in a multi-fasta file',)
    parser.add_argument('--version','-V',action='version',version='%(prog)s {}.{}'.format(script_version,script_subversion))
    parser.add_argument('filename', help="Provide a multi-fasta file that needs to be analyzed. Designed for Locus Extrator's 'mismatch_DNA'")
    parser.add_argument('--split',action='store_true', help="Separate sequences based on locus inferred from name before counting")
    parser.add_argument('--save_split',action='store_true',help="Create multi-fasta files for each gene that is identified in the file")
    parser.add_argument('--gene_part','-gp',type=int,default=1,help='Number of underscores preceeding the gene name in the output file')
    args = parser.parse_args()    
    filename = args.filename
    seqs = SeqIO.parse(filename,'fasta')
    genelists = split_LE_mismatch_file(seqs,args.gene_part) if (args.split or args.save_split) else {'All':seqs}
    for gene,g_seq in genelists.items():
        if args.save_split:
            outfile = utilities.appendToFilename(filename,"_"+gene)
            print("Saving to "+outfile)
            SeqIO.write(g_seq,outfile,'fasta')    
        g_counts = count_allele_occurances(g_seq)
        for k,v in g_counts.items():
            k.description = "{} observations".format(v)
        count_outfile = utilities.appendToFilename(filename,"_"+gene+'_counts')            
        SeqIO.write([x for x in g_counts.keys()],count_outfile,'fasta')        

##Seqs is an iterable that will produce SeqRecords
def split_LE_mismatch_file(seqs,gene_part):    
    genelists = defaultdict(list)
    for s in seqs:
        parts = s.id.split('_') ##This comes from LocusExtractor Genome_genome_similarityIinfo...
        gene = parts[gene_part] if (len(parts[1]) > 0) else "partial_"+parts[2] ##Some genomes use underscore as replacement for single quote to indicate partial gene
        if gene.startswith('-'): ##A hack from replacing underscore with dash (underscore being used as designation for partial since prime is illegal)
            gene = gene.replace('-','partial_') 
        if gene[0].isupper(): ##Peptides are distinguished by upper case. I used an underscore in a gene name ... Hi_adk
            gene += '_pep'
        genelists[gene].append(s)
    return genelists

##Seqs is an iterable that will produce SeqRecords
def count_allele_occurances(seqs):
    allele_counts = defaultdict(int)
    for s in seqs:
        found = False
        for r in allele_counts:
            if str(s.seq) == str(r.seq):
                allele_counts[r] += 1
                found = True
                print('{} matches {}'.format(s.id,r.id))
        if not found:
            allele_counts[s] += 1
    return allele_counts    
        
if __name__ == "__main__":
    if not utilities.has_preferred_python():
        raise Exception("Upgrade your python version")
    main()
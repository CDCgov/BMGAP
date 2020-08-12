#!/bin/bash
source /etc/profile

#############################################################
# Setting up pipeline for running on cluster
#############################################################
#$ -o Nm-fa_Typing_Log.out # name of .out file
#$ -e Nm-fa_Typing_Log.err # name of .err file
##$ -N Nm-fa_Typing # Rename the job to be this string instead of the default which is the name of the script
#$ -pe smp 12-16 # number of cores to use from 4-16
#$ -q all.q # where to direct query submission
#$ -cwd
#$ -m abe -M yqd9@cdc.gov #email start, abort and end of run
#echo "I am running multi threaded with $NSLOTS" 1>&2
#date
#date1=$(date +"%s")
#############################################################
#############################################################

# used to get sequence and genes for making images.
# uses

##############################################################
# ID-ing Nm sero-type
##############################################################
#echo "*** Identifying Nm sero-type ***"
#load blast module
module load ncbi-blast+/2.2.30
# make a temp list of fastq files in directory
#ls -d *fa > temp.fa.txt
ls -d *-contigs.fasta | sed -r 's/.{14}$//' > temp.fa.txt
#ls -d *fas >> temp.fa.txt
# typing using blast
FILE=temp.fa.txt
#
UTIL=${1}
NMDB="${UTIL}/TypingTab/Cap_2015_05/Capfas2"
TT="${UTIL}/TypingTab"
while read line

do

    output="$(
    blastn -db $NMDB/sodC_NEIS1339.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/galE_NEIS0048.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/A_csaA_NEIS2157.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/A_csaB_NEIS2158.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/A_csaC_NEIS2159.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/A_csaD_NEIS2160.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/B_csb_NEIS2161.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/BCWY_cssA_NEIS0054.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/BCWY_cssB_NEIS0053.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/BCWY_cssC_NEIS0052.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/BCWY_ctrG_NEIS0049.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/Nm_Gsml.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/C_csc_NEIS0051.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/C_cssE_NEIS0050.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/E_cseA_NEIS2165.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/E_cseB_NEIS2166.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/E_cseC_NEIS2167.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/E_cseD_NEIS2168.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/E_cseE_NEIS2169.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/E_cseF_NEIS2170.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/E_cseG_NEIS2171.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/H_cshC_NEIS2177.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/H_cshD_NEIS2178.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/HZ_cszA_NEIS2173.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/HZ_cszB_NEIS2174.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/I_csiC_NEIS2181.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/IK_csiA_NEIS2179.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/IK_csiB_NEIS2180.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/IK_csiD_NEIS2182.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/IK_csiE_NEIS2183.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/K_cskC_NEIS2190.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/L_cslA_NEIS2184.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/L_cslB_NEIS2185.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/L_cslC_NEIS2186.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/W_csw_NEIS2162.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/WY_cssF_NEIS2164.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/X_csxA_NEIS2187.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/X_csxB_NEIS2188.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/X_csxC_NEIS2189.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/Z_cszC_NEIS2175.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/Z_cszD_NEIS2176.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/ctrA_NEIS0055.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/ctrB_NEIS0056.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/ctrC_NEIS0057.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/ctrD_NEIS0058.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/tex_NEIS0059.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    blastn -db $NMDB/Nm_16S_rDNA.fas -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null
    )"
    echo "$output" | sort -t',' -k 2,2 -n -r -k 10,10

done < $FILE

rm temp.fa.txt
###########################################################

exit

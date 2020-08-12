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
HIDB="${Util}/haemophilus"
TT="${Util}/TypingTab"

while read line

do
    output="$(
    blastn -db $HIDB/Ref_Hi2 -query $line-contigs.fasta -evalue 1e-30 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 | $TT/Contig-Seq-Extract-External.pl $line -  2>/dev/null

    )"
    echo "$output" | sort -t',' -k 2,2 -n -r -k 10,10

done < $FILE

rm temp.fa.txt
###########################################################

exit

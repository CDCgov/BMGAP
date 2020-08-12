#!/bin/bash -l

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
echo "I am running multi threaded with $NSLOTS" 1>&2
date
date1=$(date +"%s")
#############################################################
#############################################################


##############################################################
# ID-ing Nm sero-type
##############################################################
echo "*** Identifying Nm sero-type ***"
#load blast module
module load ncbi-blast+/2.2.30
# make a temp list of fastq files in directory
#ls -d *fa > temp.fa.txt
ls -d M*.fasta | sed -r 's/.{6}$//' > temp.fa.txt
#ls -d *fas >> temp.fa.txt
# typing using blast
FILE=temp.fa.txt
# 
#FNAME=$(pwd | awk -F'/' '$0=$(NF)')
while read line
  do 
    echo "Processing $line.fasta"
blastn -db /scicomp/groups/OID/NCIRD-OD/OI/ncbs/projects/Meningitis/Nm/Typing/Cap_2015_05/Capfas2/Region_A.fas -query $line.fasta -evalue 1e-100 -num_threads 16 -outfmt '6 qseqid sseqid pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_alignments 1 >$line-RegTmp.out
##############################################################
#Serogroup results
##############################################################
perl /scicomp/home/yqd9/ncbs/projects/Meningitis/Nm/carraige-study-2015-Nm-RI/LorList/A/Parse_SPAdes_Blast.pl "$line"-RegTmp.out > "$line"-RegParse.out
#(head -n 1 "$line"-AllCapParse.out && tail -n +2 "$line"-AllCapParse.out | sort -t$'\t' -k 15,15 -n -r -k 9,9 ) > "$line"-AllCap.out
(head -n 1 "$line"-RegParse.out && tail -n +2 "$line"-RegParse.out | sort -t$'\t' -k 15,15 -n -k 9,9 ) > "$line"_RegCap.out
sed -n '1,1 p' "$line"_RegCap.out > "$line"_Reg-AllCap.out
done < $FILE

rm temp.fa.txt
#rm *.ftr
#rm *temp.fas
#unload blast module
#module unload ncbi-blast+/2.2.29
##############################################################
##############################################################

##############################################################
# Remove temp files
##############################################################
echo "*** Removing temporary files **"
#rm *-reads.*

date2=$(date +"%s")
diff=$(($date2-$date1))
echo "$(($diff / 60)) minutes and $(($diff % 60)) seconds elapsed"
##############################################################
##############################################################

exit

#!/bin/bash
source /etc/profile

#############################################################
# Defining variables
#############################################################
HOMESTART=${1}
UTIL=${2}
RUN=${3}
FOLD=${4}
SAMP=${5}
IDENT=${6}
STATE=${7}

#############################################################
# Fastqc of processed data
##############################################################
echo -e "*** FastQC Processed Reads ***" >> "$HOMESTART/Log/process.log"
echo -e "QCProc_Srt\t`date`\t`date +"%s"`" >> "$HOMESTART/Log/timing.log"
date
# Load fastqc module
module load fastqc/0.10.1
echo -e "module load fastqc/0.10./1" >> "$HOMESTART/Log/process.log"
# make a temp list of fastq files in directory
ls -d *.trim.fq | sed -r 's/.{8}$//' > temp.dedup.fq.txt
# adapter and quality trimming using cutadapt (path.*.dedup.fq)
i=1
FILE=temp.dedup.fq.txt
# FILE=temp.path.dedup.fq.txt
while read line
  do
    echo "Processing $line"
fastqc "$line".trim.fq --outdir=$HOMESTART/FASTQC-Results/
echo -e "fastqc "$line".trim.fq --outdir=$HOMESTART/FASTQC-Results/" >> "$HOMESTART/Log/process.log"
    ((i++))
done < $FILE
echo -e "QCProc_End\t`date`\t`date +"%s"`" >> "$HOMESTART/Log/timing.log"
rm temp.dedup.fq.txt

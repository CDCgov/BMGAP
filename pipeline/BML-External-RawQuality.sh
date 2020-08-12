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
# FastQC on pre-processed data
#############################################################
# making FASTQC-Results Folder
if [[ -d $HOMESTART/FASTQC-Results ]]; then
    echo "Directory FASTQC-Results exists!!"
else
    mkdir $HOMESTART/FASTQC-Results
fi

# runnng FastQC
echo -e "*** Running FastQC on pre-processed data ***" >> "$HOMESTART/Log/process.log"
echo -e "QCRaw_Srt\t`date`\t`date +"%s"`" >> "$HOMESTART/Log/timing.log"
ls -d *.fastq.gz | sed -r 's/.{3}$//' > temp.fastq.txt
# Load fastqc module
module load fastqc/0.10.1
echo -e "module load fastqc/0.10.1" >> "$HOMESTART/Log/process.log"
FILE=temp.fastq.txt
while read line
  do
    echo "Processing $line"
fastqc "$line".gz --outdir=$HOMESTART/FASTQC-Results/
done < $FILE
echo -e "QCRaw_End\t`date`\t`date +"%s"`" >> "$HOMESTART/Log/timing.log"
rm temp.fastq.txt

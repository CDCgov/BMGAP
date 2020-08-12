#!/bin/bash
# Title: BML-External-QCresults.sh
# Description: Pull out read counts from each steps of qc
# Usage:
# Date Created: 2020-06-12
# Author: Xiaoyu Sherry Zheng (qiu5@cdc.gov)



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
MONGOHOST=${8}
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
echo -e "*** Getting results/read count from previous QC steps ***" >> "$HOMESTART/Log/process.log"
echo -e "QCresults\t`date`\t`date +"%s"`" >> "$HOMESTART/Log/timing.log"
ls -d *.fastq.gz | sed -r 's/.{9}$//' > temp.txt
i=0
results=[]
FILE=temp.txt
while read line
  do
    echo "Processing $line"
results[i]=`awk '/Total Sequences/ {print $3}' $HOMESTART/FASTQC-Results/${line}_fastqc/fastqc_data.txt`
((i++))
done < $FILE
# Host read count
echo "Get host read number"
results[2]=$(grep -c ^"+" $SAMP.Host.1.fq)
results[3]=$(grep -c ^"+" $SAMP.Host.2.fq)
# Calculate host read %
hostreadp=$(echo "scale=4; ${results[2]}*100/${results[0]}" | bc)
# Pathogen read COUNT
echo "Get pathogen read number"
results[4]=$(grep -c ^"+" $SAMP.path.1.fq)
results[5]=$(grep -c ^"+" $SAMP.path.2.fq)
# Read count after trimming
echo "Get read number after triming"
results[6]=$(grep -c ^"+" $SAMP.path.1.trim.fq)
results[7]=$(grep -c ^"+" $SAMP.path.2.trim.fq)
echo -e "QCResults_End\t`date`\t`date +"%s"`" >> "$HOMESTART/Log/timing.log"
rm temp.txt

ml mongo/3.4.4
mongo --quiet --port 27017 --username 'bmgap-writer' --password "$BMGAP_WRITER_PASS" --host $MONGOHOST BMGAP --eval 'db.internal.findOneAndUpdate({"identifier":"'$IDENT'"},{"$set":{QCresults:{RawReadNumber:"'${results[0]}'",HostReadNumber:"'${results[2]}'",PathogenReadNumber:"'${results[4]}'",PosttrimReadNumber:"'${results[6]}'",HostReadPercent:"'${hostreadp}'"}}},
{upsert: true, setDefaultsOnInsert: 1, new: 1})'
echo -e "QCResults_Ingestion_End\t`date`\t`date +"%s"`" >> "$HOMESTART/Log/timing.log"

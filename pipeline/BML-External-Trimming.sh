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
# adapter, and quality trimming
# remove addapter(s), filter for Phred quality 20
##############################################################
echo -e "*** Adapter and Quality Trimming ***" >> "$HOMESTART/Log/process.log"
echo -e "Trim_Srt\t$(date)\t$(date +"%s")" >> "$HOMESTART/Log/timing.log"
date
# Load cutadapt, and fastqc module
module load cutadapt/1.8
module load Python2/2.7.13
source "${UTIL}/bmgap/bin/activate"
echo -e "module load cutadapt/1.8" >> "$HOMESTART/Log/process.log"
set -e
cutadapt -q 20 -a "file:$UTIL/Primers2Trim.fasta" -A "file:$UTIL/Primers2Trim.fasta" --times 10 -o "$SAMP".path.1.trim.fq -p "$SAMP".path.2.trim.fq "$SAMP".path.1.fq "$SAMP".path.2.fq
set +e
echo -e "cutadapt -q 20 -a file:$UTIL/Primers2Trim.fasta -A file:$UTIL/Primers2Trim.fasta --times 10 -o $SAMP.path.1.trim.fq -p $SAMP.path.2.trim.fq $SAMP.path.1.fq $SAMP.path.2.fq" >> "$HOMESTART/Log/process.log"
echo -e "Trim_End\t$(date)\t$(date +"%s")" >> "$HOMESTART/Log/timing.log"

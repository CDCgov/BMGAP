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
# Host removal using bowtie2 of human (h19), to execute this
# program launch from within the directory of fastq.gz files
##############################################################
echo -e "*** Processing fastq files to remove host ***"  >> "$HOMESTART/Log/process.log"
echo -e "HostRmv_Srt\t`date`\t`date +"%s"`" >> "$HOMESTART/Log/timing.log"
date
# file must be in name_L001_R1_001.fastq & name_L001_R2_001.fastq format
echo -e "*** Aligning fastq files with Bowtie2 ***" >> "$HOMESTART/Log/process.log"
# Load the bowtie2 aligner module
module load bowtie2/2.3.3.1
echo -e "module load bowtie2/2.3.3.1" >> "$HOMESTART/Log/process.log"
# align fastq using bowtie2
# perform bowtie2 alignment for each pair read in directory
echo -e "bowtie2 -p12 --local -t --quiet -x $UTIL/bowtie_references/bmgap_bowtie_reference -1 $SAMP_L009_R1_001.fastq -2 $SAMP_L009_R2_001.fastq --un-conc $SAMP.pathogen.fq --al-conc $SAMP.Host.fq" >> "$HOMESTART/Log/process.log"
bowtie2 -p12 --local -t --quiet -x $UTIL/bowtie_references/bmgap_bowtie_reference -1 "$SAMP"*R1_001.fastq.gz -2 "$SAMP"*R2_001.fastq.gz --un-conc "$SAMP".pathogen.fq --al-conc "$SAMP".Host.fq >"$HOMESTART/Log/bowtie2-output" 2>&1

cat "$SAMP".pathogen.1.fq | awk '{if (/^@/) print $1; else print $0}' > "$SAMP".path.1.fq
cat "$SAMP".pathogen.2.fq | awk '{if (/^@/) print $1; else print $0}' > "$SAMP".path.2.fq
rm ./*.pathogen*
echo -e "HostRmv_End\t`date`\t`date +"%s"`" >> "$HOMESTART/Log/timing.log"

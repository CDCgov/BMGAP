#!/bin/bash
source /etc/profile
export MODULEPATH=${MODULEPATH}:/apps/x86_64/easybuild/modules/all
ml --ignore-cache Skesa/2.3.0
ml --ignore-cache Python/3.7.2-GCCcore-8.2.0

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

source $UTIL/bmgap/bin/activate
echo -e "*** Running Skesa on fasatq files **" >> "$HOMESTART/Log/process.log"
echo -e "Ska_Srt\t`date`\t`date +"%s"`" >> "$HOMESTART/Log/timing.log"
echo "Sample is $SAMP"
# Running Skesa on fastq files (path.*.dedup.trim.fq)
date1=$(date +"%s")
if [[ ! -d "Skesa_$SAMP" ]]; then
    mkdir "Skesa_$SAMP"
fi
cd "Skesa_$SAMP"

# perform Skesa assembly for paired reads
echo -e "skesa --cores 16 --reads $SAMP.path.1.trim.fq,$SAMP.path.2.trim.fq --contigs_out Skesa_$SAMP_contigs.fasta" >> "$HOMESTART/Log/process.log"
set -e
skesa --cores 16 --fastq "$HOMESTART/$SAMP.path.1.trim.fq","$HOMESTART/$SAMP.path.2.trim.fq" --contigs_out "$SAMP.skesa_contigs.fasta"
set +e

cd "$HOMESTART"
echo -e "Ska_End\t`date`\t`date + %s`" >> "$HOMESTART/Log/timing.log"
date2=$(date +"%s")
diff=$(($date2-$date1))
echo "(($diff / 60)) minutes and (($diff % 60)) seconds elapsed" >> "$HOMESTART/Log/timing.log"

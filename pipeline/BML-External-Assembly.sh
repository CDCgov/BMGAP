#!/bin/bash
source /etc/profile
export MODULEPATH=${MODULEPATH}:/apps/x86_64/easybuild/modules/all
ml --ignore-cache SPAdes/3.13.1-GCC-8.2.0-2.31.1
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
echo -e "*** Running SPAdes on fasatq files **" >> "$HOMESTART/Log/process.log"
echo -e "SPA_Srt\t`date`\t`date +"%s"`" >> "$HOMESTART/Log/timing.log"
# Running SPAdes on fastq files (path.*.dedup.trim.fq)
# Load the SPAdes assembler module
date1=$(date +"%s")
echo -e "module load SPAdes/3.13.0" >> "$HOMESTART/Log/process.log"
if [[ ! -d "SPAdes_$SAMP" ]]; then
    mkdir SPAdes_"$SAMP"
fi
# perform SPades assembly for paired reads
echo -e spades.py -t 16 -m 32 --pe1-1 "$SAMP".path.1.trim.fq --pe1-2 "$SAMP".path.2.trim.fq -o SPAdes_"$SAMP" >> "$HOMESTART/Log/process.log"
set -e
spades.py -t 8 -m 32 --pe1-1 "$SAMP".path.1.trim.fq --pe1-2 "$SAMP".path.2.trim.fq -o SPAdes_"$SAMP"
set +e
cd "$HOMESTART"

echo -e "SPA_End\t`date`\t`date + %s`" >> "$HOMESTART/Log/timing.log"
date2=$(date +"%s")
diff=$(($date2-$date1))
echo "(($diff / 60)) minutes and (($diff % 60)) seconds elapsed" >> "$HOMESTART/Log/timing.log"

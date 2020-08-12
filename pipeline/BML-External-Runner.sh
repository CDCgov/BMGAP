#!/bin/bash

#############################################################
# Run this script inside folder with fq paired data
#############################################################

#############################################################
# Setting cluster
#############################################################
#$ -q all.q # where to direct query submission
#$ -o BML_AssPipe-Log.out # name of .out file
#$ -e BML_AssPipe-Log.err # name of .err file
#$ -pe smp 8 # number of cores to use from 4-16
#$ -l mem_free=32G
#$ -cwd
echo "I am running multi threaded with $NSLOTS in $PWD" 1>&2

#############################################################
# Load Modules & helper functions
#############################################################
source /etc/profile
module load mongo/3.4.4

#############################################################

#############################################################
# Starting NGS Pipeline
#############################################################
# Starting Process log file
date1=$(date +"%s")
dateStart=$(date)

#############################################################
# Defining variables
#############################################################
HOMESTART=$(pwd)
UTIL=${1}
MONGOHOST=${2}
RUN=$(dirname "$PWD" | sed 's#.*/##')
FOLD=$(pwd |sed 's#.*/##')
RAWSAMP=$(ls -d *R1_001.fastq.gz | sed -r 's/_R1.*$//')
if [[ $RAWSAMP =~ _L00? ]]; then
    SAMP=$(echo "$RAWSAMP" | sed -r 's/_L00.$//')
else
    SAMP=$RAWSAMP
fi
echo "Working on $SAMP"
STATE=$(pwd | awk -F'[/]' '{print $(NF-2)}')
PIPELINE_VERSION=$(cat "${UTIL}/pipeline_version")

#Load required libraries
source "$UTIL/BML-common-functions.sh"
ml Python/3.7
source "${UTIL}/bmgap/bin/activate"
if [[ ! -f identifier ]]; then
    NEW_ID=$(get_latest_id "$MONGOHOST")
    echo "$NEW_ID" > identifier
    COUNT=1
    FASTQ_PATH="$HOMESTART/*R1*fastq.gz"
    "$UTIL/insert_new_sample.py" -d "$MONGOHOST" -i "$NEW_ID" -c "$COUNT" -s "$STATE" -r "$FASTQ_PATH"
fi
IDENT=$(head identifier)
echo -e "$HOMESTART ${FOLD} ${UTIL} ${SAMP}"


#############################################################
# Making Log Folder
#############################################################
if ! [[ -d $HOMESTART/Log ]]; then
    mkdir "$HOMESTART/Log"
fi

#############################################################
# Making Sample and Version Logs
#############################################################
> "$HOMESTART/Log/timing.log"
> "$HOMESTART/Log/ingestion.log"
echo -e "Analyzing files with pipeline version ${PIPELINE_VERSION}" > "$HOMESTART/Log/process.log"
echo -e "BML_Pipe\t$SAMP\t$HOSTNAME" >> "$HOMESTART/Log/Node.log"
echo -e "Run_Srt\t$dateStart\t$date1" >> "$HOMESTART/Log/timing.log"
echo -e "Run_Srt\t$dateStart\t$date1" >> "$HOMESTART/Log/process.log"

"$UTIL/BML-External-Metadata.sh" "${HOMESTART}" "${UTIL}" "${RUN}" "${FOLD}" "${SAMP}" "${IDENT}" "${STATE}" "${MONGOHOST}"

if [[ $? -gt 0 ]]; then
    echo -e "${HOMESTART}\tError in inserting metadata" >>"$HOMESTART/Log/errors.log"
    restart_job "${UTIL}" "${MONGOHOST}" "${SAMP}""${STATE}" >> "$HOMESTART/Log/process.log"
    exit 1
fi

"$UTIL/BML-External-RawQuality.sh" "$HOMESTART" "$UTIL" "$RUN" "$FOLD" "$SAMP" "$IDENT" "$STATE"

if [[ $? -gt 0 ]]; then
    echo -e "${HOMESTART}\tError in inserting quality" >>"$HOMESTART/Log/errors.log"
    restart_job "${UTIL}" "${MONGOHOST}" "${SAMP}""${STATE}" >> "$HOMESTART/Log/process.log"
    exit 1
fi

"$UTIL/BML-External-HostRemoval.sh" "$HOMESTART" "$UTIL" "$RUN" "$FOLD" "$SAMP" "$IDENT" "$STATE"

if [[ $? -gt 0 ]]; then
    echo -e "${HOMESTART}\tError in removing host reads\t${REMOVAL_EXIT}" >>"$HOMESTART/Log/errors.log"
    restart_job "${UTIL}" "${MONGOHOST}" "${SAMP}""${STATE}" >> "$HOMESTART/Log/process.log"
    exit 1
fi

"$UTIL/BML-External-Trimming.sh" "$HOMESTART" "$UTIL" "$RUN" "$FOLD" "$SAMP" "$IDENT" "$STATE"

if [[ $? -gt 0 ]]; then
    echo -e "${HOMESTART}\tError in trimming" >>"$HOMESTART/Log/errors.log"
    restart_job "${UTIL}" "${MONGOHOST}" "${SAMP}""${STATE}" >> "$HOMESTART/Log/process.log"
    exit 1
fi

"$UTIL/BML-External-ProcQuality.sh" "$HOMESTART" "$UTIL" "$RUN" "$FOLD" "$SAMP" "$IDENT" "$STATE"

if [[ $? -gt 0 ]]; then
    echo -e "${HOMESTART}\tError in inserting quality" >>"$HOMESTART/Log/errors.log"
    restart_job "${UTIL}" "${MONGOHOST}" "${SAMP}""${STATE}" >> "$HOMESTART/Log/process.log"
    exit 1
fi

# Add a step to get stats from all previous QC steps/ Xiaoyu Zheng 061120
"$UTIL/BML-External-QCresults.sh" "$HOMESTART" "$UTIL" "$RUN" "$FOLD" "$SAMP" "$IDENT" "$STATE" "$MONGOHOST"

if [[ $? -gt 0 ]]; then
    echo -e "${HOMESTART}\tError in inserting QC results" >>"$HOMESTART/Log/errors.log"
    restart_job "${UTIL}" "${MONGOHOST}" "${SAMP}""${STATE}" >> "$HOMESTART/Log/process.log"
    exit 1
fi

"$UTIL/BML-External-Assembly.sh" "$HOMESTART" "$UTIL" "$RUN" "$FOLD" "$SAMP" "$IDENT" "$STATE"
if [[ $? -gt 0 ]]; then
    echo -e "${HOMESTART}\tError in inserting assembly" >>"$HOMESTART/Log/errors.log"
    restart_job "${UTIL}" "${MONGOHOST}" "${SAMP}""${STATE}" >> "$HOMESTART/Log/process.log"
    exit 1
fi

"$UTIL/BML-External-AssemblyCleanup.sh" "$HOMESTART" "$UTIL" "$RUN" "$FOLD" "$SAMP" "$IDENT" "$STATE" "$MONGOHOST"

if [[ $? -gt 0 ]]; then
    echo -e "${HOMESTART}\tError in inserting cleanup" >>"$HOMESTART/Log/errors.log"
fi

"$UTIL/BML-External-Mash.sh" "$HOMESTART" "$UTIL" "$RUN" "$FOLD" "$SAMP" "$IDENT" "$STATE" "$MONGOHOST"

if [[ $? -gt 0 ]]; then
    echo -e "${HOMESTART}\tError in inserting mash" >>"$HOMESTART/Log/errors.log"
fi

"$UTIL/BML-External-PMGA.sh" "$HOMESTART" "$UTIL" "$RUN" "$FOLD" "$SAMP" "$IDENT" "$STATE" "$MONGOHOST"

if [[ $? -gt 0 ]]; then
    echo -e "${HOMESTART}\tError in inserting PMGA" >>"$HOMESTART/Log/errors.log"
fi

LOCUS_EXIT=$UTIL/BML-External-LocusExtractor.sh "$HOMESTART" "$UTIL" "$RUN" "$FOLD" "$SAMP" "$IDENT" "$STATE" "$MONGOHOST"

if [[ $? -gt 0 ]]; then
    echo -e "${HOMESTART}\tError in inserting locus extractor" >>"$HOMESTART/Log/errors.log"
fi

"$UTIL/BML-External-Finisher.sh" "$HOMESTART" "$UTIL" "$RUN" "$FOLD" "$SAMP" "$IDENT" "$STATE" "$MONGOHOST"

if [[ $? -gt 0 ]]; then
    echo -e "${HOMESTART}\tError in finish procedure" >>"$HOMESTART/Log/errors.log"
fi

##############################################################
# Finishing Pipe run
##############################################################
echo "*** Removing temporary files **"
date2=$(date +"%s")
dateEnd=$(date)
diff=$(($date2-$date1))
echo -e "Run_END\t$dateEnd\t$date2" >> "$HOMESTART/Log/timing.log"
echo "(($diff / 60)) minutes and (($diff % 60)) seconds elapsed" >> "$HOMESTART/Log/timing.log"
##############################################################
##############################################################

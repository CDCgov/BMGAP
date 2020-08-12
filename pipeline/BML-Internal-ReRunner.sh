#!/bin/bash
#$ -q all.q # where to direct query submission

#############################################################
# Run this script inside folder with fq paired data
#############################################################

#############################################################
# Setting cluster
#############################################################
#$ -o BML_AssPipe-Log.out # name of .out file
#$ -e BML_AssPipe-Log.err # name of .err file
#$ -pe smp 12 # number of cores to use from 4-16
#$ -l mem_free=16G
#$ -cwd
##$ -M ylb9@cdc.gov #nnw8@cdc.gov,yqd9@cdc.gov
##$ -m ea #email (abe) abort, begin, and end of run
echo "I am running multi threaded with $NSLOTS" 1>&2
date
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
RUN=$(dirname $PWD | sed 's#.*/##')
FOLD=$(pwd |sed 's#.*/##')
SAMP=$(ls -d *R1_001.fastq.gz | sed -r 's/.{21}$//')
IDENT=$(head identifier)
STATE=$(pwd | awk -F'[/]' '{print $(NF-2)}')
MODULE=${3}

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
> "$HOMESTART/Log/$SAMP.log"
> "$HOMESTART/Log/$SAMP.ver.log"
> "$HOMESTART/Log/$SAMP.ingestion.log"

echo -e "BML_Pipe\t$SAMP\t$HOSTNAME" >> "$HOMESTART/Log/Node.log"
echo -e "Run_Srt\t$dateStart\t$date1" >> "$HOMESTART/Log/$SAMP.log"
echo -e "Run_Srt\t$dateStart\t$date1" >> "$HOMESTART/Log/$SAMP.ver.log"



if [[ $MODULE == "metadata" ]]; then
	$UTIL/BML-External-Metadata.sh ${HOMESTART} ${UTIL} ${RUN} ${FOLD} ${SAMP} ${IDENT}  ${MONGOHOST}

	if [[ $? -gt 0 ]]; then
	    echo -e "${HOMESTART}\tError in inserting metadata" >>$UTIL/ReRun.log
	fi
fi


if [[ $MODULE == "Cleanup" ]]; then
    $UTIL/BML-External-AssemblyCleanup.sh $HOMESTART $UTIL $RUN $FOLD $SAMP $IDENT $STATE $MONGOHOST
    if [[ $? -gt 0 ]]; then
        echo -e "${HOMESTART}\tError in inserting assembly cleanup" >>$UTIL/ReRun.log
    fi
fi

if [[ $MODULE == "mash" ]]; then
  if [[ -e SPAdes_*/*mash.tsv ]]; then
  	rm -r SPAdes_*/*mash.tsv
  fi
	MASH_EXIT=`$UTIL/BML-External-Mash.sh $HOMESTART $UTIL $RUN $FOLD $SAMP $IDENT $STATE $MONGOHOST`

	if [[ $? -gt 0 ]]; then
	    echo -e "${HOMESTART}\tError in inserting mash" >>$UTIL/ReRun.log
	fi
fi

if [[ $MODULE == "PMGA" ]]; then
	$UTIL/BML-External-PMGA.sh $HOMESTART $UTIL $RUN $FOLD $SAMP $IDENT $STATE $MONGOHOST

	if [[ $? -gt 0 ]]; then
	    echo -e "${HOMESTART}\tError in inserting PMGA" >>$UTIL/ReRun.log
	fi
fi

if [[ $MODULE == "Locus" ]]; then
	rm -r SPAdes*/Locus*
	$UTIL/BML-External-LocusExtractor.sh $HOMESTART $UTIL $RUN $FOLD $SAMP $IDENT $STATE $MONGOHOST

	if [[ $? -gt 0 ]]; then
	    echo -e "${HOMESTART}\tError in inserting Locus Extractor" >>$UTIL/ReRun.log

	fi
fi
##############################################################
# Finishing Pipe run
##############################################################
echo "*** Removing temporary files **"
date2=$(date +"%s")
dateEnd=$(date)
diff=$(($date2-$date1))
echo -e "Run_END\t$dateEnd\t$date2" >> $HOMESTART/Log/$SAMP.log
echo "$(($diff / 60)) minutes and $(($diff % 60)) seconds elapsed" >> $HOMESTART/Log/$SAMP.log

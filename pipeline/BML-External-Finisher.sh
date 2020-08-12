#!/bin/bash
#
# Title: BML-External-Finisher.sh
# Description:
# Usage:
# Date Created: 2019-02-08 16:13
# Author: Reagan Kelly (ylb9@cdc.gov)
# Last Modified: Jun 16 2020 by Xiaoyu Zheng (qiu5@cdc.gov)
# Changes: Added increment to the samples_running field in runs


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

echo -e "*** Running Finishing Procedure **" >> "$HOMESTART/Log/process.log"
echo -e "Finish\t$SAMP\t$HOSTNAME" >> "$HOMESTART/Log/Nodes.log"
echo -e "Finish_Srt\t$(date)\t$(date +"%s")" >> "$HOMESTART/Log/timing.log"

echo "$RUN" "$SAMP"
if [[ $RUN == test_run && $SAMP == M11111_Q08 ]]; then
    exit 0
fi

source /etc/profile
module load mongo/3.4.4
export MODULEPATH=${MODULEPATH}:/apps/x86_64/easybuild/modules/all
ml --ignore-cache Python/3.7.2-GCCcore-8.2.0
source "${UTIL}/bmgap/bin/activate"
source "${UTIL}/BML-common-functions.sh"
python "${UTIL}/add_read_path_field.py" "${MONGOHOST}" "${SAMP}" >>"$HOMESTART/Log/process.log"
CONSISTENCY=$("$UTIL/check_sample_consistency.py" "$IDENT" "$MONGOHOST")
COMPLETION=$("$UTIL/check_sample_completion.py" -i "$IDENT" -d "$MONGOHOST")
python "$UTIL/sample_summary_collection.py" -i "$IDENT" -d "$MONGOHOST" >> "$HOMESTART/Log/process.log"
$UTIL/update_sample_order.sh

if [[ $COMPLETION =~ Complete || $COMPLETION == \["fwdReadPath"\] ]]; then
    mongo --quiet --port 27017 --username 'bmgap-writer' --password "$BMGAP_WRITER_PASS" --host "$MONGOHOST" BMGAP --eval 'db.active_runs.updateOne({"Run_ID": "'"$RUN"'"},{$inc: {count: -1}, $pull: {samples: "'"$IDENT"'"}})'
    # update number of active running sample in this run
    mongo --quiet --port 27017 --username 'bmgap-writer' --password "$BMGAP_WRITER_PASS" --host "$MONGOHOST" BMGAP --eval 'db.runs.updateOne({"run": "'"$RUN"'"},{$inc: {samples_running: -1}})'
    echo -e "$SAMP finished" >> "$HOMESTART/Log/timing.log"
else
   JOB_INFO=$(qsub $UTIL/backfill_sample.sh $UTIL $MONGOHOST)
   send_incomplete_email "$SAMP" "$COMPLETION\n$JOB_INFO"
   echo -e "$COMPLETION missing" >> "$HOMESTART/Log/timing.log"
   exit 1
fi

if [[ $CONSISTENCY == "false" ]]; then
   echo -e "$SAMP has a consistency issue"
   echo -e "Subject: $SAMP has a consistency issue \n\n Check it out.\n" | /usr/sbin/sendmail -f qiu5@cdc.gov qiu5@cdc.gov
fi

"$UTIL/BML-Run-Finisher.sh" "$UTIL" "$RUN" "$MONGOHOST"
echo -e "Finish_End\t$(date)\t$(date +"%s")" >> "$HOMESTART/Log/timing.log"

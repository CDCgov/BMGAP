#!/bin/bash
#
# Title: BML-External-Finisher.sh
# Description:
# Usage:
# Date Created: 2019-02-08 16:13
# Author: Reagan Kelly (ylb9@cdc.gov)
# Last Modified: Jun 16 2020 by Xiaoyu Zheng (qiu5@cdc.gov)
# Modifications: replace Reagan's email address with Xiaoyu's; Set samples_running to 0 if whole run has finished.

source /etc/profile
ml mongo/3.4.4

#############################################################
# Defining variables
#############################################################
UTIL=${1}
RUN=${2}
MONGOHOST=${3}
source "${UTIL}/BML-common-functions.sh"

total_run_count=$(mongo --quiet --port 27017 --username 'bmgap-writer' --password "$BMGAP_WRITER_PASS" --host "$MONGOHOST" BMGAP --eval 'db.active_runs.find({"Run_ID": "'"$RUN"'"}).count()')

total_sample_count=$("$UTIL/jq_standalone" '.count' <(mongo --quiet --port 27017 --username 'bmgap-writer' --password "$BMGAP_WRITER_PASS" --host "$MONGOHOST" BMGAP --eval 'db.active_runs.findOne({"Run_ID": "'"$RUN"'"},{_id: 0, count: 1})'))
echo $total_run_count $total_sample_count
if [[ $total_run_count -gt 0 && $total_sample_count -eq 0 ]]; then
    EMAIL_LIST=("ymw8@cdc.gov" "noc0@cdc.gov" "lyi3@cdc.gov" "wwg2@cdc.gov" "pnz9@cdc.gov" "nva3@cdc.gov" "qiu5@cdc.gov")
    #EMAIL_LIST=("qiu5@cdc.gov")
    for addr in "${EMAIL_LIST[@]}"; do
        send_completion_email "${RUN}" "${addr}"
    done
    mongo --quiet --port 27017 --username 'bmgap-writer' --password "$BMGAP_WRITER_PASS" --host "$MONGOHOST" BMGAP --eval 'db.active_runs.deleteOne({"Run_ID": "'"$RUN"'"})'
    mongo --quiet --port 27017 --username 'bmgap-writer' --password "$BMGAP_WRITER_PASS" --host "$MONGOHOST" BMGAP --eval 'db.runs.updateOne({"run": "'"$RUN"'"}, {$set: {"analysis_running": false, "samples_running": 0}})'
    #if [[ $QC_STATUS =~ Passed ]]; then
    #    echo -e "Passed QC, adding to Mash sketch" >> "$HOMESTART/Log/process.log"
    #    cd "$UTIL/bmgap_mash_sort/"
    #    python3 "$UTIL/bmgap_mash_sort/update_mash_sketch.py" -m "$MASH_SKETCH" -f "$ASSEMBLY_PATH" -t 6 >> "$HOMESTART/Log/process.log"
    #    echo -e $(ls -ltr "$MASH_SKETCH") >> "$HOMESTART/Log/process.log"
    #fi
elif [[ $total_run_count -eq 0 ]]; then
    echo "Run not being tracked"
elif [[ $total_sample_count -gt 0 ]]; then
    echo "Some samples still need to be analyzed"
fi

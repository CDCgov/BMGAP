#!/bin/bash
source /etc/profile
export MODULEPATH=${MODULEPATH}:/apps/x86_64/easybuild/modules/all
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
MONGOHOST=${8}
PIPELINE_VERSION=$(cat "${UTIL}/pipeline_version")
#############################################################
#Add metadata (Run ID, State, etc.) to placeholder
#############################################################
module load mongo/3.4.4
source ${UTIL}/BML-common-functions.sh
source ${UTIL}/bmgap/bin/activate

BMlog1=$(mongo --quiet --port 27017 --username 'bmgap-writer' --password "$BMGAP_WRITER_PASS" --host $MONGOHOST BMGAP --eval 'db.internal.find({"identifier":"'$IDENT'"})')
var1='{  }'

if [[ $BMlog1 == $var1 ]]; then
   echo -e "Error in creating a placeholder in the database. Probable cause of error is that this placeholder already exist in database.\n" >> $HOMESTART/Log/ingestion.log
else
    echo "Placeholder created" >> $HOMESTART/Log/ingestion.log
fi

SAMPLE_ORDER=$(get_sample_order $SAMP)

mongo --quiet --port 27017 --username 'bmgap-writer' --password "$BMGAP_WRITER_PASS" --host $MONGOHOST BMGAP --eval 'db.internal.findOneAndUpdate({"identifier":"'$IDENT'"},{"$set":{Run_ID:"'$RUN'",Assembly_ID:"'$SAMP'",Lab_ID: "'$FOLD'",location:"'$HOMESTART'",version:"'$PIPELINE_VERSION'",sample_order:"'$SAMPLE_ORDER'", meta:{Submitter_Country:"USA",Submitter_State:"'$STATE'"}}},{upsert: true, setDefaultsOnInsert: true, new: true})'
deactivate

#!/bin/bash

source /etc/profile
ml mongo/3.4.4

if [[ -z ${1} ]]; then
    UTIL=~/pipelines/bmgap/external
else
    UTIL=${1}
fi

if [[ -z ${2} ]]; then
    MONGOHOST=bmgap-poc.biotech.cdc.gov
else
    MONGHOST=${2}
fi

source $UTIL/BML-common-functions.sh
IDENTIFIER=$(cat identifier)
SAMPLE_ORDER=$(get_sample_order $(get_sample_name))
echo $SAMPLE_ORDER
mongo --quiet --host $MONGOHOST --port 27017 --username bmgap-writer --password "$BMGAP_WRITER_PASS" BMGAP --eval 'db.internal.update({identifier: "'$IDENTIFIER'"}, {$set: {sample_order: '$SAMPLE_ORDER'}})'
mongo --quiet --host $MONGOHOST --port 27017 --username bmgap-writer --password "$BMGAP_WRITER_PASS" BMGAP --eval 'db.sample_summary.update({identifier: "'$IDENTIFIER'"}, {$set: {sample_order: '$SAMPLE_ORDER'}})'

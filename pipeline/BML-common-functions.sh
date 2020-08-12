#!/bin/bash
#
# Title: BML-common-functions.sh
# Description:
# Usage:
# Date Created: 2019-01-28 15:48
# Author: Reagan Kelly (ylb9@cdc.gov)
# Last Modified: Thu 02 Jul 2020 09:54:06 AM EDT
# Last Modified by: Xiaoyu Sherry Zheng (qiu5@cdc.gov)
# Modification: Updated email address and email sending setting


get_latest_id () {
    MONGO_HOST=${1}
    BMcount=$(mongo --quiet --port 27017 --username 'bmgap-reader' --password="$MONGO_READER_PASS" --host "$MONGO_HOST" BMGAP --eval 'db.internal.find({},{"_id":0,"identifier":1}).limit(1).sort({"identifier" : -1})')
    A=$(echo "$BMcount" | cut -d'M' -f2 | cut -d'"' -f1)
    A=$((10#${A}+1))
    B=$(printf "%05d" $A)
    echo "BM$B"
}

strip_quotes () {
    VAR=${1}
    TMP=${VAR%\"}
    echo "${TMP#\"}"
}

finish () {
    echo "Finishing"
}

clear_database_record () {
    SCRIPT_PATH=${1}
    MONGO_HOST=${2}
    LAB_ID=${3}
    SUBMITTER=${4}
    RECORD_COUNT=$(mongo --quiet --port 27017 --username 'bmgap-reader' --password "$MONGO_READER_PASS" --host "${MONGO_HOST}" BMGAP --eval 'db.internal.find({"Lab_ID": "'"${LAB_ID}"'"}).count()')
    if [[ $RECORD_COUNT -gt 0 ]]; then
        record=$(mongo --quiet --port 27017 --username 'bmgap-reader' --password "$MONGO_READER_PASS" --host "${MONGO_HOST}" BMGAP --eval 'printjson(db.internal.findOne({"Lab_ID": "'"${LAB_ID}"'"},{_id: 0}))')
        identifier=$("$SCRIPT_PATH/jq_standalone" '.identifier' <<< "$record")

        count=$(mongo --quiet --username 'bmgap-reader' --password "$MONGO_READER_PASS" --host "${MONGO_HOST}" BMGAP --eval 'db.internal.find({identifier: '$identifier'}).count()')
        if [[ $count -eq 1 ]]; then
            mongo --quiet --username 'bmgap-writer' --password "$BMGAP_WRITER_PASS" --host "${MONGO_HOST}" BMGAP --eval 'db.internal.remove({identifier: '$identifier'})'
            source "$SCRIPT_PATH/bmgap/bin/activate"
            "$SCRIPT_PATH/insert_new_sample.py" -d "$MONGO_HOST" -i "$identifier" -c "$count" -s "$SUBMITTER"
            echo "Successfully cleared and recreated database entry"
        fi
    fi
}

restart_job () {
    SCRIPT_PATH=${1}
    MONGO_HOST=${2}
    LAB_ID=${3}
    SUBMITTER=${4}
    clear_database_record "${SCRIPT_PATH}" "${MONGO_HOST}" "${LAB_ID}" "${SUBMITTER}"
    /opt/sge/bin/lx-amd64/qsub "${SCRIPT_PATH}/BML-External-Runner.sh" "${SCRIPT_PATH}" "${MONGO_HOST}"
}


send_completion_email () {
    RUN=${1}
    EMAIL_ADDR=${2}
    MSG="Subject: Run $RUN seems to be finished\n\n Check to make sure it looks ok"
    send_email "${MSG}" "${EMAIL_ADDR}"
}

send_incomplete_email () {
    SAMPLE=${1}
    MISSING_FIELDS=${2}
    EMAIL_ADDR=${3}
    if [[ -z $EMAIL_ADDR ]]; then
        EMAIL_ADDR=qiu5@cdc.gov
    fi
    MSG="Subject: Analysis for $SAMPLE did not complete successfully\n\n The sample is missing $MISSING_FIELDS"
    send_email "${MSG}" "${EMAIL_ADDR}"
}

send_start_email () {
    RUN=${1}
    COUNT=${2}
    EMAIL_ADDR=${3}
    MSG="Subject: Started analysis for $RUN \n\n There are $COUNT samples in this run. The system will send another email when the run analysis is finished"
    echo $MSG
    send_email "${MSG}" "${EMAIL_ADDR}"
}

send_email () {
    MSG=${1}
    EMAIL_ADDR=${2}
    echo -e $MSG >~/mailbody
    /usr/sbin/sendmail -f no-reply@cdc.gov $EMAIL_ADDR <~/mailbody
}

get_sample_order () {
    ID_VALUE=${1}
    if [[ $ID_VALUE =~ .*_S[0-9]+$ ]]; then
        ORDER=${ID_VALUE##*_S}
        echo $ORDER
    fi
}

get_sample_name () {
    if [[ -f *R1_001.fastq.gz ]]; then
        RAWSAMP=$(ls -d *R1_001.fastq.gz | sed -r 's/_R1.*$//')
        if [[ $RAWSAMP =~ _L00? ]]; then
            SAMP=$(echo $RAWSAMP | sed -r 's/_L00.$//')
        else
            SAMP=$RAWSAMP
        fi
    else
        SAMP=$(get_assembly_id $(cat identifier))
    fi
    echo $SAMP
}

get_assembly_id () {
    ID_VALUE=${1}
    UTIL=${2}
    MONGOHOST=${3}
    echo "$ID_VALUE $UTIL $MONGOHOST"
    ml mongo/3.4.4
    mongo --quiet --host $MONGOHOST --username 'bmgap-reader' --password "$MONGO_READER_PASS" BMGAP --eval 'db.internal.findOne({identifier: "'$ID_VALUE'"}, {_id: 0, Assembly_ID: 1})'
    RECORD=$(mongo --quiet --host $MONGOHOST --username 'bmgap-reader' --password "$MONGO_READER_PASS" BMGAP --eval 'db.internal.findOne({identifier: "'$ID_VALUE'"}, {_id: 0, Assembly_ID: 1})')
    echo $RECORD
}

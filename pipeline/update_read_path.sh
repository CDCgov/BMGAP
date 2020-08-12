#!/usr/bin/env bash

source /etc/profile
ml mongo/3.4.4

if [[ -z ${1} ]]; then
    exit 1
fi

if [[ -z ${2} ]]; then
    exit 1
fi

IDENTIFIER=${1}
FILEPATH=${2}

mongo --host bmgap-poc.biotech.cdc.gov --username bmgap-writer --password "$BMGAP_WRITER_PASS" --port 27017 BMGAP --eval 'db.internal.updateOne({identifier: "'$IDENTIFIER'"}, {$set: {fwdReadPath: "'$FILEPATH'"}})'

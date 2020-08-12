#!/bin/bash

source /etc/profile
ml Python/3.7

BMGAP_PIPELINE=${1}
MONGOHOST=${2}

source $BMGAP_PIPELINE/bmgap/bin/activate

echo "Checking run $(basename $PWD)"

while read line; do
    pushd $line >/dev/null 2>&1
    STATUS=$(python $BMGAP_PIPELINE/check_sample_completion.py -i $(cat identifier) -d $MONGOHOST)
    if [[ $STATUS != '["Complete"]' ]]; then
        echo "$line is missing $STATUS"
        if [[ $STATUS =~ cleanData ]]; then
            echo "Assembly is bad"
        else
            qsub $BMGAP_PIPELINE/backfill_sample.sh
        fi
    fi
    popd >/dev/null 2>&1
done<k

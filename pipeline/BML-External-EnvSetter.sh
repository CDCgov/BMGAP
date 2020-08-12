#!/usr/bin/env bash
export HOMESTART=$(pwd)
export UTIL=${1}
export MONGOHOST=${2}
export RUN=$(dirname "$PWD" | sed 's#.*/##')
export FOLD=$(pwd |sed 's#.*/##') 
export SAMP=$(ls -d *R1_001.fastq.gz | sed -r 's/.{21}$//')
export IDENT=$(head identifier)
export STATE=$(pwd | awk -F'[/]' '{print $(NF-2)}')

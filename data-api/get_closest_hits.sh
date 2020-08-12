#!/bin/bash -l
#
# Title: get_closest_hits.sh
# Description:
# Usage:
# Date Created: 2018-11-13 12:37
# Last Modified: Thu 11 Jul 2019 05:58:55 PM EDT
# Author: Reagan Kelly (ylb9@cdc.gov)
#

assemblyPath=${1}
mashSketch=${2}
module load Mash/2.0
module load Python/3.4
python3 "${PWD}/bmgap_mash_sort/get_closest_hits.py" -f $assemblyPath -m $mashSketch

#!/usr/bin/env bash
#
# Title: make_phylo_tree.sh
# Description:
# Usage:
# Date Created: 2019-01-22 11:59
# Last Modified: Tue 01 Oct 2019 02:34:50 PM EDT
# Author: Reagan Kelly (ylb9@cdc.gov)
#

assembly_fofn=${1}
source /etc/profile
export MODULEPATH=${MODULEPATH}:/apps/x86_64/easybuild/modules/all
ml Mash/2.0
ml --ignore-cache Python/3.7.2-GCCcore-8.2.0
source /opt/bmgap/bmgap/bin/activate

python3 "${PWD}/phylo_tree_scripts/build_phylo_fast_bmgap.py" -i $assembly_fofn -t 4 >scratch_file 2>&1
tree_name=$(ls -t my_tree* | head -n1 |tr -d \n | tr -d \' )
if [[ -e $tree_name ]]; then
    cat $tree_name
else
    exit 1
fi

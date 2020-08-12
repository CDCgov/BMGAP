#!/bin/bash
source /etc/profile

#############################################################
# Defining variables
#############################################################
HOMESTART=${1}
echo ${2}
UTIL=${2}
echo ${3}
RUN=${3}
echo ${4}
FOLD=${4}
echo ${5}
SAMP=${5}
echo ${6}
IDENT=${6}
STATE=${7}
MONGOHOST=${8}

#############################################################
# PMGA
#############################################################
export MODULEPATH=${MODULEPATH}:/apps/x86_64/easybuild/modules/all
ml --ignore-cache Python/3.7.2-GCCcore-8.2.0
module load mongo/3.4.4
module load ncbi-blast+/LATEST
module load Mash/2.0

source "$UTIL/bmgap/bin/activate"

echo -e "*** PMGA**" >> "$HOMESTART/Log/process.log"
echo -e "PMGA\t$SAMP\t$HOSTNAME" >> "$HOMESTART/Log/Nodes.log"
source ${UTIL}/bmgap/bin/activate
echo -e "source ${UTIL}/bmgap/bin/activate" >> "$HOMESTART/Log/process.log"
#echo -e $HOSTNAME >> "$HOMESTART/Log/timing.log"
echo -e "PMGA_Srt\t`date`\t`date +"%s"`" >> "$HOMESTART/Log/timing.log"


# Running PMGA
cd SPAdes*
#cd Skesa*
if [ -d ./dummy ]; then
    echo "Directory dummy exists!!"
else
    mkdir dummy
fi

cp "$SAMP"_cleaned.fasta dummy/

#echo -e "python $UTIL/PMGA/build_pubmlst_dbs.py -o $UTIL/PMGA/pubmlst_dbs_all " >> "$HOMESTART/Log/process.log"
#python $UTIL/PMGA/build_pubmlst_dbs.py -o $UTIL/PMGA/pubmlst_dbs_all

if [ -d ./PMGA/json ]; then
    echo "PMGA json directory exists!! using -jf flag" >> "$HOMESTART/Log/process.log"
    echo -e "python $UTIL/PMGA/blast_pubmlst.py -d dummy/ -b $UTIL/PMGA/pubmlst_dbs_all -sg -t 80 -jf PMGA/json -o PMGA/ " >> "$HOMESTART/Log/process.log"
    python3 $UTIL/PMGA/blast_pubmlst.py -d dummy/ -b $UTIL/PMGA/pubmlst_dbs_all -sg -t 80 -jf PMGA/json -o PMGA/ >> "$HOMESTART/Log/process.log"
else
    echo -e "python $UTIL/PMGA/blast_pubmlst.py -d dummy/ -b $UTIL/PMGA/pubmlst_dbs_all -sg -t 80 -o PMGA/ " >> "$HOMESTART/Log/process.log"
    python3 $UTIL/PMGA/blast_pubmlst.py -d dummy/ -b $UTIL/PMGA/pubmlst_dbs_all -sg -t 80 -o PMGA/ >> "$HOMESTART/Log/process.log"
fi



cd PMGA
PMGAPATH=$(pwd -P)

mongo --quiet --port 27017 --username 'bmgap-writer' --password "$BMGAP_WRITER_PASS" --host $MONGOHOST BMGAP --eval 'db.internal.findOneAndUpdate({"identifier":"'$IDENT'"},{"$set":{PMGA:{"filejson":"'${PMGAPATH}/json/${SAMP}_cleaned_final_results.json'","filegff":"'${PMGAPATH}/gff/${SAMP}_cleaned.gff'"}}})'
python $UTIL/dataIngestionPMGAJSON.py $PMGAPATH/serogroup $IDENT $MONGOHOST >> "$HOMESTART/Log/process.log"
python $UTIL/dataIngestionPMGA.py $PMGAPATH/serogroup $IDENT $MONGOHOST >> "$HOMESTART/Log/process.log"
echo -e "PMGA_End\t`date`\t`date +"%s"`" >> "$HOMESTART/Log/timing.log"
deactivate

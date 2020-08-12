#!/bin/bash
source /etc/profile

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

#############################################################
# Locus Extractor
#############################################################
module load mongo/3.4.4

echo -e "*** Running Locus Extractor **"  "$HOMESTART/Log/process.log"
echo -e "LE\t$SAMP\t$HOSTNAME" >> "$HOMESTART/Log/Nodes.log"
echo -e $HOSTNAME >> "$HOMESTART/Log/timing.log"
echo -e "LEx_Srt\t`date`\t`date +"%s"`" >> "$HOMESTART/Log/timing.log"


# check for locusextractor program
if [ -d ./locusextractor ]; then
    rm -rf ./locusextractor
fi

cp -rf $UTIL/locusextractor ./
cp -f $UTIL/reference_sequences.tar.gz locusextractor
cd locusextractor
tar -xzf reference_sequences.tar.gz
cd ..

# Running Locus Extractor
ml ncbi-blast+/2.2.29 Python/3.7
echo -e "module load ncbi-blast+/2.2.29" >> "$HOMESTART/Log/process.log"
cd SPAdes*
#cd Skesa*
if [[ -d LocuseExtractor* ]]; then
    rm -r LocusExtractor*
fi
echo -e "python3 ../locusextractor/LocusExtractor.py "$SAMP"_cleaned.fasta $SAMP" >> "$HOMESTART/Log/process.log"
python3 ../locusextractor/LocusExtractor.py --no_update "$SAMP"_cleaned.fasta $SAMP > $SAMP.LE.log

cd Loc*
LEPATH=$(pwd -P)
export MODULEPATH=${MODULEPATH}:/apps/x86_64/easybuild/modules/all
ml --ignore-cache Python/3.7.2-GCCcore-8.2.0
source ${UTIL}/bmgap/bin/activate
echo -e "source ${UTIL}/bmgap/bin/activate" >> "$HOMESTART/Log/process.log"
python3 $UTIL/dataIngestionLocusExtractor.py $LEPATH $IDENT $MONGOHOST

#MLST logging code
BMlog5=$(mongo --quiet --port 27017 --username 'bmgap-writer' --password "$BMGAP_WRITER_PASS" --host ${MONGOHOST} BMGAP --eval 'db.internal.find({"identifier":"'$IDENT'"},{"_id":0,"MLST.Lab_ID":1}).limit(1).sort({$natural : -1})')
var1='{  }'

if [[ $BMlog5 == $var1 ]]; then
    echo -e "Error in Locusextractor insertion module.\n"   >> $HOMESTART/Log/ingestion.log
else
    echo "Locusextractor ingestion finished"
fi

python3 "${UTIL}/add_assembly_path_field.py" "${MONGOHOST}"  "${SAMP}"

#cd $HOMESTART/SPAdes*
echo -e "LEx_End\t`date`\t`date +"%s"`" >> "$HOMESTART/Log/timing.log"
deactivate

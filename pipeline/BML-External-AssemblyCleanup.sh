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
#Setup output folders to copy to
#############################################################
BASE_OUTPATH=BMGAP/Instruments

if [[ ${HOMESTART} == */HiSeq/* ]]; then
    OUTFOLDER=${BASE_OUTPATH}/HiSeq
elif [[ ${HOMESTART} == */MiSeq/* ]]; then
    OUTFOLDER=${BASE_OUTPATH}/MiSeq
elif [[ ${HOMESTART} == */BML_MiSeq/* ]]; then
    OUTFOLDER=${BASE_OUTPATH}/BML_MiSeq
elif [[ ${HOMESTART} == */external/* ]]; then
    OUTFOLDER=${BASE_OUTPATH}/external/${STATE}
else
    OUTFOLDER=${HOMESTART}
fi

#############################################################
# Assembly Cleanup
#############################################################
module load mongo/3.4.4
ml Python/3.7

echo -e "*** Running AssemblyCleanup **" >> "$HOMESTART/Log/process.log"
echo -e "Clean\t$SAMP\t$HOSTNAME" >> "$HOMESTART/Log/Nodes.log"
#echo -e $HOSTNAME >> "$HOMESTART/Log/timing.log"
echo -e "AssClean_Srt\t`date`\t`date +"%s"`" >> "$HOMESTART/Log/timing.log"

source "${UTIL}/bmgap/bin/activate"
echo -e "activate python virtualenv" >> "$HOMESTART/Log/process.log"

# Copy AssemblyCleanup if it does not exist
if [ -d ./AssemblyCleanup ]; then
    echo "Directory AssemblyCleanup exists!!"
else
    cp -rf $UTIL/AssemblyCleanup ./
fi

# Running Assembly Cleanup
cd SPAdes*
if [ -f  $SAMP.fasta.report.tab ]; then
    python3 $UTIL/dataIngestionAssemblyCleanup.py $SAMP.fasta.report.tab $IDENT "${OUTFOLDER}/${RUN}/AssemblyCleanup/" $MONGOHOST >> "$HOMESTART/Log/process.log"
else
    python3 ../AssemblyCleanup/cleanupSingle.py -c 0 -p 0.1 -b $SAMP contigs.fasta $SAMP.fasta  >> "$HOMESTART/Log/process.log"
    echo -e "python3 ../AssemblyCleanup/cleanupSingle.py -c 0 -p 0.1 -b $SAMP contigs.fasta $SAMP.fasta" >> "$HOMESTART/Log/process.log"
    python3 $UTIL/dataIngestionAssemblyCleanup.py $SAMP.fasta.report.tab $IDENT "${OUTFOLDER}/${RUN}/AssemblyCleanup/" $MONGOHOST >> "$HOMESTART/Log/process.log"
    $UTIL/update_qc_flag.py $MONGOHOST $IDENT
fi

mkdir -p ${OUTFOLDER}/${RUN}/AssemblyCleanup
mv $SAMP.fasta "$SAMP"_cleaned.fasta
echo -e "Renamed cleaned file" >> "$HOMESTART/Log/process.log"
cp "$SAMP"_cleaned.fasta $OUTFOLDER/$RUN/AssemblyCleanup/
cp $SAMP.fasta.report.png $OUTFOLDER/$RUN/AssemblyCleanup/
cp "$SAMP"_discarded.fasta $OUTFOLDER/$RUN/AssemblyCleanup/
cp $SAMP.fasta.report.tab $OUTFOLDER/$RUN/AssemblyCleanup/

echo -e "Moved files" >> "$HOMESTART/Log/process.log"
cd $HOMESTART
echo -e "AssClean_End\t`date`\t`date +"%s"`" >> "$HOMESTART/Log/timing.log"
deactivate

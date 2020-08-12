#!/bin/bash
source /etc/profile
ml Python/3.7

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
BASEDIR=$(dirname $HOMESTART)
BMGAP_RESULTS='./by-instrument'
MASH_SKETCH="${BMGAP_RESULTS}/full_mash_sketch/BMGAP_DATA_MASH_DB.msh"

#############################################################
# MASH
#############################################################

echo -e "*** Mash/2.0"
echo -e "MASH\t$SAMP\t$HOSTNAME" >> "$HOMESTART/Log/Nodes.log"
echo -e "MASH_Srt\t`date`\t`date +"%s"`" >> "$HOMESTART/Log/timing.log"

source ${UTIL}/bmgap/bin/activate
ml Mash/2.0
ml mongo/3.4.4
echo -e "source ${UTIL}/bmgap/bin/activate" >> "$HOMESTART/Log/process.log"
echo -e "module load Mash/2.0"

# Running MASH
cd SPAdes*
CLEAN_FASTA=$(ls $SAMP*_cleaned.fasta)
if [[ -e $CLEAN_FASTA ]]; then
  echo $CLEAN_FASTA
  echo -e "python $UTIL/MASH/SpeciesDB/bin/identify_species_bmgap.py $CLEAN_FASTA > $SAMP.mash.tsv" >> "$HOMESTART/Log/process.log"
  python "$UTIL/MASH/SpeciesDB/bin/identify_species_bmgap.py" "$CLEAN_FASTA" > "$SAMP".mash.tsv
  MASHING=$(tail -n1 "$SAMP.mash.tsv")
  MASHfoo=(`echo "$MASHING" | sed 's/,/\n /g'`}) #do we need "}" in this line
  SPECIES=$(echo "$MASHING" | cut -d"," -f2)

  echo -e "${MASHING}" >> "$HOMESTART/Log/process.log"
  echo -e "${MASHfoo[4]}" >> "$HOMESTART/Log/process.log"

  mongo --quiet --port 27017 --username 'bmgap-writer' --password "$BMGAP_WRITER_PASS" --host $MONGOHOST BMGAP --eval 'db.internal.findOneAndUpdate({"identifier":"'$IDENT'"},{"$set":{mash:{Top_Species:"'${MASHfoo[1]}_${MASHfoo[2]}'",Notes:"'${MASHfoo[3]}'",
  Mash_Dist:"'${MASHfoo[4]}'",Mash_P_value:"'${MASHfoo[5]}'",Mash_Hash:"'${MASHfoo[6]}'",Mash_Entry:"'${MASHfoo[7]}'",Mash_Entry_Source:"'${MASHfoo[8]}'"}}},
  {upsert: true, setDefaultsOnInsert: 1, new: 1})'
  #Mash logging code
  BMlog3=$(mongo --quiet --port 27017 --username 'bmgap-writer' --password "$BMGAP_WRITER_PASS" --host $MONGOHOST BMGAP --eval 'db.internal.find({"identifier":"'$IDENT'"},{"_id":0,"mash.Top_Species":1}).limit(1).sort({$natural : -1})')

  var1='{  }'

  if [[ $BMlog3 == $var1 ]]; then
      echo -e "Error in Mash insertion module.\n"  >> "$HOMESTART/Log/ingestion.log"
  else
      echo "Mash ingestion finished"
  fi

  NMSPECIES="Neisseria meningitidis"
  HISPECIES="Haemophilus influenzae"
  if [[ "$SPECIES" = "$NMSPECIES" ]]
      then
      "$UTIL/Gene_Extract_External.sh" "$UTIL" > "genes.out"
      echo "$NMSPECIES"
  elif [[ "$SPECIES" = "$HISPECIES" ]]
      then
      "$UTIL/Gene_Extract_External_HI.sh" "$UTIL" > "genes.out"
      echo "$HISPECIES"
  else
      echo "NOT HI or NM"
  fi


  GENE=$(cat genes.out)
  if [[ "$GENE" = "" ]]
      then
      echo -e "Empty genes.out file" >> "$HOMESTART/Log/process.log"
  else
      GENEPATH=$(pwd -P)
      python3 "$UTIL/dataIngestionGenes.py" "$GENEPATH" "$IDENT" "${MONGOHOST}"
  fi
  echo -e "Done ingesting genes, check qc" >> "$HOMESTART/Log/process.log"
  RECORD=$(mongo --quiet --port 27017 --username 'bmgap-writer' --password "$BMGAP_WRITER_PASS" --host $MONGOHOST BMGAP --eval 'db.internal.find({"identifier":"'$IDENT'"},{"_id":0}).limit(1).sort({$natural : -1})')
  QC_STATUS=$("$UTIL/jq_standalone" '.cleanData | .Status' <<< "$RECORD")
  echo -e "QC Status = $QC_STATUS" >>$HOMESTART/Log/process.log
  ASSEMBLY_PATH=$("$UTIL/jq_standalone" '.assemblyPath' <<< "$RECORD")
  echo -e $ASSEMBLY_PATH >>$HOMESTART/Log/process.log

  cd "$HOMESTART"
  echo -e "MASH_END\t`date`\t`date +"%s"`" >> "$HOMESTART/Log/timing.log"
  deactivate
fi

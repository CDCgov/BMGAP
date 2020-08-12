#!/bin/bash

#############################################################
# Defining variables
#############################################################
while getopts "s:d:omcriple" opt; do
    case $opt in
        s)
            UTIL=$OPTARG
            ;;
        d)
            MONGOHOST=$OPTARG
            ;;
        o)
            OVERWRITE=TRUE
            ;;
        m)
            METADATA=TRUE
            ;;
        c)
            CLEANUP=TRUE
            ;;
        r)
            SERO=TRUE
            ;;
        i)
            MASH=TRUE
            ;;
        p)
            PMGA=TRUE
            ;;
        l)
            LOCUS_EXTRACTOR=TRUE
            ;;
        e)
            METADATA=TRUE
            CLEANUP=TRUE
            SERO=TRUE
            MASH=TRUE
            PMGA=TRUE
            LOCUS_EXTRACTOR=TRUE
            ;;
    esac
done

if [[ -z $UTIL || -z "$MONGOHOST" ]]; then
    exit "Script dir and db host required"
fi
HOMESTART=$(pwd)
RUN=$(dirname $PWD | sed 's#.*/##')
FOLD=$(pwd |sed 's#.*/##')
SAMP=$(ls -d *R1_001.fastq.gz | sed -r 's/.{21}$//')
if [[ -e identifier ]]; then
    IDENT=$(head identifier)
else
    IDENT=$(get_latest_id $MONGOHOST)
fi
STATE=$(pwd | awk -F'[/]' '{print $(NF-2)'})

#############################################################
#Load necessary modules
#############################################################
source $UTIL/BML-common-functions.sh
source /etc/profile
ml Python/3.7
if ! [[ $(hostname) =~ "ncbs-submit" ]]; then
  module load mongo/3.4.4
fi
module load ncbi-blast+/2.6.0


#############################################################
#Check if identifier already exists
#############################################################
if [[ -n "$IDENT" ]]; then
    REC_COUNT=$(mongo --quiet --port 27017 --username 'bmgap-writer' --password "$BMGAP_WRITER_PASS" --host "$MONGOHOST" BMGAP --eval 'db.internal.find({"identifier":"'$IDENT'"}).count()')
    echo $REC_COUNT
    if [[ $REC_COUNT -gt 0 ]]; then
        mongo --quiet --port 27017 --username 'bmgap-writer' --password="$BMGAP_WRITER_PASS" --host "$MONGOHOST" BMGAP --eval 'db.internal.find({"identifier":"'$IDENT'"}, {"_id": 0})' >example.json
        RUN_ID=$(strip_quotes "$("$UTIL/jq_standalone" '.Run_ID' <example.json)")
        SAMPLE_ID=$(strip_quotes "$("$UTIL/jq_standalone" '.Lab_ID' <example.json)")
        if [[ $RUN == "$RUN_ID" && $FOLD == "$SAMPLE_ID" ]]; then
            echo "Right run, right sample"
            if [[ $OVERWRITE != TRUE ]]; then
                exit 0
            fi
        else
            echo "$RUN not $RUN_ID $FOLD not $SAMPLE_ID"
            IDENT=$(get_latest_id $MONGOHOST)
            echo "$IDENT" >identifier
            $UTIL/insert_new_sample.py -d "$MONGOHOST" -i $IDENT
        fi
    fi
else
    echo "$IDENT" >identifier
    $UTIL/insert_new_sample.py -d "$MONGOHOST" -i $IDENT
fi

#############################################################
#Insert Metadata
#############################################################
if [[ $METADATA = TRUE ]]; then
    echo "Loading Metadata"
    mongo --quiet --port 27017 --username 'bmgap-writer' --password "$BMGAP_WRITER_PASS" --host "$MONGOHOST" BMGAP --eval 'db.internal.findOneAndUpdate({"identifier":"'$IDENT'"}, {"$set":{Run_ID:"'$RUN'",Assembly_ID:"'$SAMP'",Lab_ID:"'$FOLD'",location : "'$HOMESTART'",meta:{Submitter_Country:"USA",Submitter_State:"'$STATE'"}}}, {upsert: true, setDefaultsOnInsert: true, new: true})' >tmpfile
fi

#############################################################
#Insert Serogrouping
#############################################################
cd SPAdes*
if [[ $SERO = TRUE ]]; then
    echo "Loading Serogrouping"
    if [[ -e $SAMP-contigs.fasta ]]; then
        NMGROUP=$($UTIL/Grouping-Nm-fasta.sh)
        NMfoo=(${NMGROUP})

        mongo --quiet --port 27017 --username 'bmgap-writer' --password "$BMGAP_WRITER_PASS" --host "$MONGOHOST" BMGAP --eval 'db.internal.findOneAndUpdate({"identifier":"'$IDENT'"},{"$set":{serogrouping:{Infer:"'${NMfoo[1]}'",
        baseSG:"'${NMfoo[4]}'", gene1:"'${NMfoo[5]}'",gene2:"'${NMfoo[6]}'",gene3:"'${NMfoo[7]}'",gene4:"'${NMfoo[8]}'",gene5:"'${NMfoo[9]}'",gene6:"'${NMfoo[10]}'",
        gene7:"'${NMfoo[11]}'"}}}, {upsert: true, setDefaultsOnInsert: 1, new: 1})' >tmpfile
    fi
fi
cd $HOMESTART

#############################################################
#Insert Serotyping
#############################################################
cd SPAdes*
if [[ $SERO = TRUE ]]; then
    echo "Loading Serotying"
    if [[ -e $SAMP-contigs.fasta ]]; then
        HITYPE=$($UTIL/haemophilus/hiping0nt $UTIL/haemophilus/Ref_Hi2 $SAMP-contigs.fasta)
        HIfoo=(${HITYPE})

        mongo --quiet --port 27017 --username 'bmgap-writer' --password "$BMGAP_WRITER_PASS" --host "$MONGOHOST" BMGAP --eval 'db.internal.findOneAndUpdate({"identifier":"'$IDENT'"},{"$set":{serotyping:{ST:"'${HIfoo[15]}'",bexA:"'${HIfoo[16]}'",
        bexB:"'${HIfoo[17]}'",bexC:"'${HIfoo[18]}'",bexD:"'${HIfoo[19]}'",hcsA:"'${HIfoo[20]}'",hcsB:"'${HIfoo[21]}'",_cs1:"'${HIfoo[22]}'",_cs2:"'${HIfoo[23]}'",_cs3:"'${HIfoo[24]}'",
        _cs4:"'${HIfoo[25]}'",_cs5:"'${HIfoo[26]}'",_cs6:"'${HIfoo[27]}'",_cs7:"'${HIfoo[28]}'",_cs8:"'${HIfoo[29]}'"}}},{upsert: true, setDefaultsOnInsert: 1, new: 1})' >tmpfile
    fi
fi
cd $HOMESTART


#############################################################
#Insert Assembly Cleanup
#############################################################
source "${UTIL}/bmgap/bin/activate"
cd SPAdes*
if [[ $CLEANUP = TRUE ]]; then
    echo "Loading Assembly Cleanup"
    if [ -f  $SAMP.fasta.report.tab ]; then
        python3 $UTIL/dataIngestionAssemblyCleanup.py $SAMP.fasta.report.tab $IDENT "${OUTFOLDER}/${RUN}/AssemblyCleanup/" "$MONGOHOST" >> $HOMESTART/Log/$SAMP.ver.log
    else
        echo -e "Assembly Cleanup Report not found"
    fi

    RECORD=$(mongo --quiet --port 27017 --username 'bmgap-writer' --password "$BMGAP_WRITER_PASS" --host "$MONGOHOST" BMGAP --eval 'db.internal.find({"identifier":"'$IDENT'"},{"_id":0}).limit(1).sort({$natural : -1})')
    QC_STATUS=$(strip_quotes $($UTIL/jq_standalone '.cleanData | .Status' <<< $RECORD))

    if [[ $QC_STATUS == "Passed" ]]; then
        FLAG_VAL="false"
    else
        FLAG_VAL="true"
    fi
    echo $QC_STATUS
    echo $FLAG_VAL
    mongo --quiet --port 27017 --username 'bmgap-writer' --password "$BMGAP_WRITER_PASS" --host "$MONGOHOST" BMGAP --eval 'db.internal.findOneAndUpdate({"identifier":"'$IDENT'"},{"$set":{"QC_flagged":"'$FLAG_VAL'"}})' >tmpfile
fi
cd $HOMESTART
deactivate


#############################################################
#Insert Mash results
#############################################################
source "${UTIL}/bmgap/bin/activate"
cd SPAdes*
if [[ $MASH = TRUE ]]; then
    echo "Loading Mash"
    GENEPATH=$(pwd -P)
    GENE=(`cat genes.out`)
    if [[ "$GENE" = "" && -f "$SAMP.mash.tsv" ]]; then
        echo "Redoing mash parsing"
        MASHING=$(tail -n1 "$SAMP.mash.tsv")
        MASHfoo=$(echo "$MASHING" | sed 's/,/\n /g') #do we need "}" in this line
        SPECIES=$(echo "$MASHING" | cut -d"," -f2)
        mongo --quiet --port 27017 --username 'bmgap-writer' --password "$BMGAP_WRITER_PASS" --host "$MONGOHOST" BMGAP --eval 'db.internal.findOneAndUpdate({"identifier":"'$IDENT'"},{"$set":{mash:
        {Top_Species:"'${MASHfoo[1]}_${MASHfoo[2]}'",Notes:"'${MASHfoo[3]}'", Mash_Dist:"'${MASHfoo[4]}'",Mash_P_value:"'${MASHfoo[5]}'",
        Mash_Hash:"'${MASHfoo[6]}'",Mash_Entry:"'${MASHfoo[7]}'",Mash_Entry_Source:"'${MASHfoo[8]}'"}}},
        {upsert: true, setDefaultsOnInsert: 1, new: 1})' >tmpfile
        NMSPECIES="Neisseria meningitidis"
        HISPECIES="Haemophilus influenzae"
        if [[ "$SPECIES" = "$NMSPECIES" ]]
            then
            echo "Neis"
            $UTIL/Gene_Extract_External.sh $UTIL > genes.out
        elif [[ "$SPECIES" = "$HISPECIES" ]]
            then
            echo "Haem"
            $UTIL/Gene_Extract_External_HI.sh $UTIL > genes.out
        fi
    fi
    if [[ ! (( $(python3 $UTIL/dataIngestionGenes.py $GENEPATH $IDENT ${MONGOHOST}) )) ]]; then
        echo "Problem with mash ingestion"
    fi
fi
cd $HOMESTART
deactivate

#############################################################
#Insert PMGA results
#############################################################
source "${UTIL}/bmgap/bin/activate"
cd SPAdes*
if [[ $PMGA = TRUE ]]; then
    echo "Loading PMGA"
    cd PMGA
    PMGAPATH=$(pwd -P)
    mongo --quiet --port 27017 --username 'bmgap-writer' --password "$BMGAP_WRITER_PASS" --host "$MONGOHOST" BMGAP --eval 'db.internal.findOneAndUpdate({"identifier":"'$IDENT'"},
        {"$set":{PMGA:{"filejson":"'${PMGAPATH}/json/${SAMP}_cleaned_final_results.json'","filegff":"'${PMGAPATH}/gff/${SAMP}_cleaned.gff'"}}})' >tmpfile

    python $UTIL/dataIngestionPMGAJSON.py $PMGAPATH/serogroup $IDENT $MONGOHOST
    python $UTIL/dataIngestionPMGA.py $PMGAPATH/serogroup $IDENT $MONGOHOST
fi
cd $HOMESTART
deactivate


#############################################################
#Insert Locus Extractor results
#############################################################
source "${UTIL}/bmgap/bin/activate"
cd SPAdes*
if [[ $LOCUS_EXTRACTOR = TRUE ]]; then
    echo "Loading LocusExtractor"
    cd Loc*
    LEPATH=$(pwd -P)
    python3 $UTIL/dataIngestionLocusExtractor.py $LEPATH $IDENT $MONGOHOST
    python3 "${UTIL}/add_assembly_path_field.py" "${MONGOHOST}"  "${SAMP}"
fi
cd $HOMESTART
deactivate

#!/usr/bin/python
# -*- coding: utf-8 -*-

from pymongo import MongoClient
import sys


def AssemblyCleanup(filename, db, identifier, assembly_path):

    try:
        with open(filename, "r") as ff:
            raw_keys = ff.readline().strip()
            raw_values = ff.readline().strip()
        keys = raw_keys.split("\t")
        values = raw_values.split("\t")
        assembly = {}

        for i in range(len(keys)):
            if values[i].startswith('"') and values[i + 1].endswith('"'):
                assembly[keys[i]] = values[i] + "," + values[i + 1]
                del values[i + 1]
            else:
                assembly[keys[i]] = values[i]

        assembly["filename"] = assembly_path + filename
        print(assembly_path + filename)

        if (
            (float(assembly["Mean_Coverage_raw"]) < 25)
            or (
                float(assembly["HalfCov_Contig_Bases"])
                / float(assembly["Bases_In_Contigs"])
            )
            > 1
            or (
                float(assembly["Bases_In_Contigs_raw"])
                - float(assembly["Bases_In_Contigs"])
            )
            / float(assembly["Bases_In_Contigs_raw"])
            > 5
        ):
            assembly["Status"] = "Failed"
        else:
            assembly["Status"] = "Passed"

        update_for_mongo = {"cleanData": assembly}

        db.internal.update_one(
            {"identifier": identifier}, {"$set": update_for_mongo}, upsert=True
        )
        ff.close()
    except OSError:
        pass


if __name__ == "__main__":
    file_name = sys.argv[1]
    id = sys.argv[2]
    output_path = sys.argv[3]
    mongo_url = sys.argv[4] if len(sys.argv) >= 5 else "bmgap-poc.biotech.cdc.gov"

    client = MongoClient(
        mongo_url, username="bmgap-writer", password="bmgap-example", authSource="BMGAP"
    )
    db_connection = client.BMGAP
    AssemblyCleanup(file_name, db_connection, id, output_path)

# usage python dataIngestionLocusExtractor.py molecular_data.csv identifer
# cd Loc*/Results_text/ then pass molecular_data.csv as argument and identifier as 2nd argument

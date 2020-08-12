#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from pymongo import MongoClient
import json
import sys


def MLST(filename, identifier):

    try:
        with open(filename, "r") as mlst_file:
            raw_molecular_data = json.load(mlst_file)

        mlst = {k: raw_molecular_data[k]["0"] for k in raw_molecular_data}

        n = mlst["Nm_MLST_ST"]
        h = mlst["Hi_MLST_ST"]
        if n == "Not applicable" and h == "Not Applicable":
            mlst["ST"] = "Not applicable"
        elif n == "Not applicable":
            mlst["ST"] = h
        elif h == "Not applicable":
            mlst["ST"] = n
        else:
            mlst["ST"] = "Not applicable"
        print(mlst)
        return mlst
    except OSError:
        pass


def update_record(identifier, db, molecular_data):
    mismatch = (
        molecular_data["mismatched_DNA"]
        if "mismatched_DNA" in molecular_data.keys()
        else ""
    )
    db.internal.update(
        {"identifier": identifier},
        {"$set": {"MLST": molecular_data["MLST"], "mismatched_DNA": mismatch}},
        upsert=True,
    )


def update_assembly_path(identifier, db):
    base_path = "./BMGAP/Instruments/"
    query = {"$or": [{"identifier": identifier}, {"Lab_ID": identifier}]}
    record = db.internal.find_one(query)
    if record:
        path_components = record["location"].split("/")[-4:]
        if path_components[0] == "external":
            run_path = "/".join(path_components[:-1])
        else:
            run_path = "/".join(path_components[1:][:-1])
        final_path = base_path + run_path
        full_path = final_path + "/AssemblyCleanup/" + record["MLST"]["Filename"]
        db.internal.update(
            {"_id": record["_id"]}, {"$set": {"assemblyPath": full_path}}
        )


def MLST_allele(filename, identifier):

    try:
        keys, values = get_kv_from_file(filename)
        mlst = {}

        for i in range(len(keys)):
            if values[i].startswith('"') and values[i + 1].endswith('"'):
                mlst[keys[i]] = values[i] + "," + values[i + 1]
                del values[i + 1]
            else:

                mlst[keys[i]] = values[i]
        return mlst

    except OSError:
        pass


def get_mismatched_data(filename, identifier):
    try:
        with open(filename, "r") as ff:
            data = ff.read()
        return data
    except OSError:
        pass


def get_kv_from_file(filename):
    with open(filename, "r") as ff:
        raw_keys = ff.readline().strip()
        raw_values = ff.readline().strip()

    keys = raw_keys.split(",")
    values = raw_values.split(",")
    return keys, values


if __name__ == "__main__":

    directory = sys.argv[1]
    identifier = sys.argv[2]
    mongo_url = sys.argv[3] if len(sys.argv) == 4 else "bmgap-poc.biotech.cdc.gov"
    client = MongoClient(
        mongo_url, username="bmgap-writer", password="bmgap-example", authSource="BMGAP"
    )
    db = client.BMGAP

    for file1 in os.listdir(os.path.join(os.getcwd(), directory)):
        if file1 == "mismatched_DNA.fasta":
            mismatched_dna = get_mismatched_data(
                os.path.join(directory, file1), identifier
            )
        if file1 == "mismatched_peptides.fasta":
            mismatched_peptide = get_mismatched_data(
                os.path.join(directory, file1), identifier
            )
        if file1 == "molecular_data.json":
            mlst = MLST(os.path.join(directory, file1), identifier)

    directory1 = directory + "/Results_text"
    for file2 in os.listdir(directory1):
        if file2 == "allele_data.csv":
            mlst_allele = MLST_allele(os.path.join(directory1, file2), identifier)

    molecular_data = {}
    try:
        molecular_data["mismatched_DNA"] = mismatched_dna
    except NameError:
        pass
    try:
        molecular_data["mismatched_peptide"] = mismatched_peptide
    except NameError:
        pass
    try:
        molecular_data["MLST"] = mlst
    except NameError:
        pass
    try:
        molecular_data["MLST_allele"] = mlst_allele
    except NameError:
        pass

    print(molecular_data.keys())
    update_record(identifier, db, molecular_data)
    update_assembly_path(identifier, db)

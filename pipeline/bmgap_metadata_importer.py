#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Title: bmgap_metadata_importer.py
Description:
Usage:
Date Created: 2018-12-19 16:35
Last Modified: Tue 30 Apr 2019 02:31:44 PM EDT
Author: Reagan Kelly (ylb9@cdc.gov)
"""

import sys
import csv
import re
from pymongo import MongoClient


def main(args, db):
    import_data = get_data_to_import(args[0])
    print(import_data[0].keys())
    for row in import_data:
        import_the_data(row, db)


def import_the_data(data_to_import, db):
    record = db.internal.find_one({"identifier": data_to_import["BMGAP_ID"]})
    if record:
        try:
            does_match = re.search(data_to_import["Lab_Id"], record["Lab_ID"])
            if does_match:
                metadata_to_import = prepare_data_for_import(data_to_import)
                db.internal.update_one(
                    {"identifier": data_to_import["BMGAP_ID"]},
                    {"$set": {"BML_Data": metadata_to_import}},
                )
        except:
            print(data_to_import["BMGAP_ID"])


def prepare_data_for_import(data_to_import):
    bml_metadata = {}
    bml_metadata["country"] = (
        data_to_import["Submitter_Country"]
        if data_to_import["Submitter_Country"] != "NULL"
        else ""
    )
    bml_metadata["state"] = (
        data_to_import["Submitter_State"]
        if data_to_import["Submitter_State"] != "NULL"
        else ""
    )
    bml_metadata["year"] = (
        data_to_import["Year_Collected"]
        if data_to_import["Year_Collected"] != "NULL"
        else ""
    )
    bml_metadata["sample_type"] = (
        data_to_import["Source_of_Specimen"]
        if data_to_import["Source_of_Specimen"] != "NULL"
        else ""
    )
    bml_metadata["lab_st"] = (
        data_to_import["CDC_SAST"] if data_to_import["CDC_SAST"] != "NULL" else ""
    )
    bml_metadata["lab_sg"] = (
        data_to_import["CDC_SASG"] if data_to_import["CDC_SASG"] != "NULL" else ""
    )
    bml_metadata["nm_pcr"] = (
        data_to_import["Nm_PCR_Results"]
        if data_to_import["Nm_PCR_Results"] != "NULL"
        else ""
    )
    bml_metadata["hi_pcr"] = (
        data_to_import["Hi_PCR_Results"]
        if data_to_import["Hi_PCR_Results"] != "NULL"
        else ""
    )
    if bml_metadata["state"]:
        bml_metadata["location"] = bml_metadata["state"]
    elif bml_metadata["country"]:
        bml_metadata["location"] = bml_metadata["country"]
    return bml_metadata


def get_data_to_import(filename):
    data_to_import = []
    with open(filename, "r") as data_file:
        reader = csv.DictReader(data_file)
        for row in reader:
            data_to_import += [row]

    return data_to_import


if __name__ == "__main__":
    if len(sys.argv) == 2:
        mongo_server = "mongodb://bmgap-poc.biotech.cdc.gov"
    else:
        mongo_server = "mongodb://" + sys.argv[1]
    client = MongoClient(
        mongo_server, username="bmgap-writer", password="bmgap-example", authSource="BMGAP"
    )
    db_connection = client.BMGAP
    main(sys.argv[2:], db_connection)

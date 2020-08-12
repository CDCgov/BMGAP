#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
#

"""
Title: make_sample_summary_collection.py
Description:
Usage:
Date Created: 2019-05-10 09:12
Last Modified: Mon 07 Oct 2019 08:14:30 PM EDT
Author: Reagan Kelly (ylb9@cdc.gov)
"""

import sys
import re
import logging
import argparse
import pymongo


def main(db, identifier):
    field_list = {
        "identifier": "identifier",
        "Lab_ID": "Lab_ID",
        "Assembly_ID": "Assembly_ID",
        "Run_ID": "Run_ID",
        "QC_flagged": "QC_flagged",
        "Submitter": "Submitter",
        "assemblyPath": "assemblyPath",
        "MLST": "MLST.ST",
        "cc": "MLST.Nm_MLST_cc",
        "Serotype": "Serotype.ST",
        "Serogroup": "Serogroup.SG",
        "location": "BML_Data.location",
        "country": "BML_Data.country",
        "year": "BML_Data.year",
        "sample_type": "BML_Data.sample_type",
        "sample_order": "sample_order",
        "Species": "mash.Top_Species",
        "sequence_flagged": "sequence_flagged",
        "assembly_flagged": "assembly_flagged",
    }
    if identifier == "all":
        summarize_all_samples(db, field_list)
    elif identifier:
        sample_summary = summarize_single_sample(db, identifier, field_list)
        db.sample_summary.update_one(
            {"identifier": identifier}, {"$set": sample_summary}, upsert=True
        )
    else:
        print("Specify which identifier to make summary for")
        sys.exit(2)


def summarize_all_samples(db, field_list):
    all_identifiers = db.internal.find({}, {"identifier": 1, "_id": 0})
    for identifier in all_identifiers:
        logging.error(identifier)
        sample_summary = summarize_single_sample(
            db, identifier["identifier"], field_list
        )
        if sample_summary:
            db.sample_summary.update_one(
                {"identifier": identifier["identifier"]},
                {"$set": sample_summary},
                upsert=True,
            )
    for field in field_list.keys():
        logging.error(field)
        db.sample_summary.create_index(
            [(field, pymongo.ASCENDING), (field, pymongo.DESCENDING)]
        )


def summarize_single_sample(db, identifier, field_list):
    new_sample_dict = {}
    rec = db.internal.find_one({"identifier": identifier})
    for name, field in field_list.items():
        if re.search("\.", field):
            fields = field.split(".")
            if fields[0] in rec and fields[1] in rec[fields[0]]:
                new_sample_dict[name] = rec[fields[0]][fields[1]]
        elif field in rec:
            new_sample_dict[name] = rec[field]
    if new_sample_dict and "Run_ID" in new_sample_dict.keys():
        logging.error(identifier)
        logging.error(new_sample_dict["Run_ID"])
        run_info = db.runs.find_one({"run": new_sample_dict["Run_ID"]})
        if run_info and "sequencer" in run_info.keys():
            new_sample_dict["sequencer"] = run_info["sequencer"]
        if (
            "mash" in new_sample_dict.keys()
            and "Notes" in new_sample_dict["mash"].keys()
        ):
            if (
                run_info["mash"]["Notes"]
                == "No_hit_above_threshold_from_reference_collection_Reporting_top_refseq_hit"
            ):
                new_sample_dict["species_flagged"] = True
            else:
                new_sample_dict["species_flagged"] = False
        if "cleanData" in new_sample_dict.keys():
            if "Mean_Coverage_raw" in new_sample_dict["cleanData"].keys():
                if new_sample_dict["cleanData"]["Mean_Coverage_raw"] < 25:
                    new_sample_dict["assembly_flagged"] = True
                    new_sample_dict["QC_flagged"] = True
                else:
                    new_sample_dict["assembly_flagged"] = False
            if (
                "HalfCov_Percent" in new_sample_dict["cleanData"].keys()
                or "Discarded_Percent" in new_sample_dict["cleanData"].keys()
            ):
                if (
                    new_sample_dict["cleanData"]["HalfCov_Percent"] > 1
                    or new_sample_dict["cleanData"]["Discarded_Percent"] > 5
                ):
                    new_sample_dict["sequence_flagged"] = True
                    new_sample_dict["QC_flagged"] = True
                else:
                    new_sample_dict["sequence_flagged"] = False
        return new_sample_dict


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # database
    parser.add_argument(
        "-d", "--db_host", action="store", default="bmgap-poc.biotech.cdc.gov"
    )
    # identifier
    parser.add_argument("-i", "--identifier", action="store", required=True)

    args = vars(parser.parse_args())
    client = pymongo.MongoClient(
        args["db_host"],
        27017,
        username="bmgap-writer",
        password="bmgap-example",
        authSource="BMGAP",
    )
    db = client.BMGAP
    main(db, args["identifier"])

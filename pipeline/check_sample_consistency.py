#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Title: 
Description:
Usage:
Date Created: 2019-01-03 18:10
Last Modified: Mon 18 Feb 2019 01:16:04 PM EST
Author: Reagan Kelly (ylb9@cdc.gov)
"""

import sys
import logging
import json
import re
import os.path
from pymongo import MongoClient


def main(args):
    if len(args) < 2:
        sys.exit(1)
    idval = args[0]
    db = get_db(args[1])
    print(idval + str(check_consistency(idval, db)))


def check_consistency(iden, db):
    record = get_record(iden, db)
    if record:
        mlst_status = check_mlst(record)
        assembly_status = check_assembly(record)
        pmga_status = check_pmga(record)
        reads_status = check_reads(record)
        if mlst_status and assembly_status and pmga_status and reads_status:
            return "true"
        else:
            return [
                x
                for x in [mlst_status, assembly_status, pmga_status, reads_status]
                if not x
            ]
    return "false"


def get_db(address):
    client = MongoClient(
        address,
        27017,
        username="bmgap-writer",
        password="bmgap-example",
        authSource="BMGAP",
    )
    return client.BMGAP


def get_record(iden, db):
    rec = db.internal.find_one({"identifier": iden})
    return rec


def check_mlst(record):
    if (
        "MLST" in record
        and "Filename" in record["MLST"]
        and re.search(record["Assembly_ID"], record["MLST"]["Filename"])
    ):
        return True
    return False


def check_assembly(record):
    if (
        "cleanData" in record
        and "Filename" in record["cleanData"]
        and re.search(record["Lab_ID"], record["cleanData"]["Filename"])
    ):
        return True
    return False


def check_pmga(record):
    if "PMGATyping" in record:
        if len(record["PMGATyping"]["Serogroup"]) > 0:
            pmga_val = record["PMGATyping"]["Serogroup"][0]
        elif len(record["PMGATyping"]["Serotype"]) > 0:
            pmga_val = record["PMGATyping"]["Serotype"][0]
        if pmga_val and re.search(record["Assembly_ID"], pmga_val["sample_name"]):
            return True
    return False


def check_reads(record):
    if "fwdReadPath" in record and os.path.exists(record["fwdReadPath"]):
        return True
    return False


def check_run(record):
    seq_date = record["Run_ID"].split("_")[0]
    if "location" in record and re.search(seq_date, record["location"]):
        return True
    return False


if __name__ == "__main__":
    main(sys.argv[1:])

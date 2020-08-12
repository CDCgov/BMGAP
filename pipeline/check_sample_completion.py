#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
#

"""
Title:check_sample_completion.py
Description:
Usage:
Date Created: 2018-12-21 11:56
Last Modified: Thu 21 Feb 2019 03:43:52 PM EST
Author: Reagan Kelly (ylb9@cdc.gov)
"""

import argparse
import sys
import logging
import json
import pymongo


def main(identifier, db, output="raw"):
    fields = [
        "PMGATyping",
        "MLST",
        "mash",
        "Run_ID",
        "assemblyPath",
        "QC_flagged",
        "location",
        "cleanData",
    ]
    sample = db.internal.find_one({"identifier": identifier})
    status = {}
    for f in fields:
        if f not in sample.keys():
            status[f] = "missing"
        elif f in sample.keys():
            status[f] = "done"
    if output == "json":
        print(json.dumps(status))
    elif output == "raw":
        missing = [k for k, v in status.items() if v == "missing"]
        if not missing:
            missing = ["Complete"]
        print(json.dumps(missing))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # database
    parser.add_argument(
        "-d", "--db_host", action="store", default="bmgap-poc.biotech.cdc.gov"
    )
    # identifier
    parser.add_argument("-i", "--identifier", action="store", required=True)
    parser.add_argument("-j", "--json_format", action="store_true", required=False)

    args = vars(parser.parse_args())
    if args["json_format"]:
        output = "json"
    else:
        output = "raw"
    client = pymongo.MongoClient(
        args["db_host"],
        27017,
        username="bmgap-writer",
        password="bmgap-example",
        authSource="BMGAP",
    )
    db = client.BMGAP
    main(args["identifier"], db, output)

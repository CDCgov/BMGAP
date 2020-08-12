#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Title: add_mlst_aggregation_function.py
Description:
Usage:
Date Created: 2018-07-06 11:47
Last Modified: Fri 15 Feb 2019 04:40:09 PM EST
Author: Reagan Kelly (ylb9@cdc.gov)
"""

from pymongo import MongoClient
import sys


def main(db):
    all_records = db.internal.find({})
    for r in all_records:
        if "MLST" in r.keys():
            st = ""
            n = r["MLST"]["Nm_MLST_ST"]
            h = r["MLST"]["Hi_MLST_ST"]
            if n == "Not applicable" and h == "Not Applicable":
                st = "Not applicable"
            elif n == "Not applicable":
                st = h
            elif h == "Not applicable":
                st = n
            else:
                st = "Not applicable"
            db.internal.update({"_id": r["_id"]}, {"$set": {"MLST.ST": st}})


if __name__ == "__main__":
    if len(sys.argv) == 1:
        mongo_server = "mongodb://bmgap-poc.biotech.cdc.gov"
    else:
        mongo_server = "mongodb://" + sys.argv[1]
    client = MongoClient(
        mongo_server, username="bmgap-writer", password="bmgap-example", authSource="BMGAP"
    )
    db_connection = client.BMGAP
    main(db_connection)

#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from pymongo import MongoClient
import json
import sys


def PMGA(filename, db, identifier):
    fname = filename
    try:
        pmga = json.load(open(filename))
        result = db.internal.update_one(
            {"identifier": identifier}, {"$set": {"PMGATyping": pmga}}, upsert=True
        )
    except OSError:
        pass


if __name__ == "__main__":
    if len(sys.argv) == 4:
        host = sys.argv[3]
    else:
        host = "mongodb://bmgap-poc.biotech.cdc.gov"
    client = MongoClient(
        host, username="bmgap-writer", password="bmgap-example", authSource="BMGAP"
    )
    db = client.BMGAP

    directory = sys.argv[1]
    identifier = sys.argv[2]
    for file1 in os.listdir(directory):
        if file1.endswith(".json"):
            PMGA(directory + "/" + file1, db, identifier)

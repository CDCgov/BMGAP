#!/usr/bin/python
# -*- coding: utf-8 -*-

import pymongo
import os
from pymongo import MongoClient
import json
from bson import json_util
import logging
import re
import sys


def PMGA(filename, db, identifier):
    fname = filename
    try:
        if fname.endswith(".tab"):
            ff = open(fname, "r")
            keys = ff.readline().strip()
            keys = keys.split("\t")
            values = ff.readline().strip()
            values = values.split("\t")
            pmga = {}
            for i in range(len(keys)):
                if values[i].startswith('"') and values[i + 1].endswith('"'):
                    pmga[keys[i]] = values[i] + "," + values[i + 1]
                    del values[i + 1]
                else:
                    pmga[keys[i]] = values[i]

            if fname.split("/")[-1].startswith("serogroup"):
                result = db.internal.update_one(
                    {"identifier": identifier},
                    {"$set": {"Serogroup": pmga}},
                    upsert=True,
                )

            if fname.split("/")[-1].startswith("serotype"):
                result = db.internal.update_one(
                    {"identifier": identifier},
                    {"$set": {"Serotype": pmga}},
                    upsert=True,
                )
            ff.close()
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
        PMGA(directory + "/" + file1, db, identifier)

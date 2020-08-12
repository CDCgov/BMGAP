#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from pymongo import MongoClient
import sys
from collections import defaultdict


def genes(filename, db, identifier):

    fname = filename
    print(fname)
    try:
        ff = open(fname, "r")
        myDict = defaultdict(lambda: defaultdict(dict))
        content = ff.read().strip()
        content = content.split("\n")
        for i in range(len(content)):
            newContent = content[i].split("\t")

            contig_num = newContent[0].split("_")
            contig = "Contig" + contig_num[1] if len(contig_num) == 2 else ""
            if len(newContent) < 20:
                break
            stops = int(newContent[18])
            seq = newContent[19]
            aper = newContent[16]
            cov = float(newContent[15])
            pid = newContent[2]
            qstart = min(int(newContent[9]), int(newContent[8]))
            qend = max(int(newContent[9]), int(newContent[8]))
            myDict[contig][newContent[1]]["start"] = qstart
            myDict[contig][newContent[1]]["end"] = qend
            myDict[contig][newContent[1]]["stop"] = stops
            myDict[contig][newContent[1]]["seq"] = seq
            myDict[contig][newContent[1]]["aper"] = aper
            myDict[contig][newContent[1]]["cov"] = cov
            myDict[contig][newContent[1]]["pid"] = pid
            alen = newContent[0].split("_")[3]
            myDict[contig]["length"] = alen

            # myDict[contig][newContent[0].split('_')[1]].append(newContent[1])

        db.internal.update_one(
            {"identifier": identifier}, {"$set": {"genes": myDict}}, upsert=True
        )

        ff.close()
    except OSError:
        pass


if __name__ == "__main__":

    directory = sys.argv[1]
    identifier = sys.argv[2]
    mongo_url = sys.argv[3] if len(sys.argv) == 4 else "bmgap-poc.biotech.cdc.gov"
    client = MongoClient(
        mongo_url, username="bmgap-writer", password="bmgap-example", authSource="BMGAP"
    )
    db = client.BMGAP

    for file1 in os.listdir(directory):
        if file1 == "genes.out":
            genes(directory + "/" + file1, db, identifier)

# usage python dataIngestionLocusExtractor.py molecular_data.csv identifer
# cd SPades* then pass directory as argument and identifier as 2nd argument

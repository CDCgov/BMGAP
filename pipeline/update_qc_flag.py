#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Title:
Description:
Usage:
Date Created: 2018-12-21 12:27
Last Modified: Tue 08 Oct 2019 10:12:13 AM EDT
Author: Reagan Kelly (ylb9@cdc.gov)
  """

import sys
from pymongo import MongoClient


def main(iden, db):
    record = db.internal.find_one({"identifier": iden})
    flag_status, sequence, assembly = get_flag_status(record)
    if flag_status is not None:
        db.internal.update_one(
            {"identifier": iden},
            {
                "$set": {
                    "QC_flagged": flag_status,
                    "assembly_flagged": assembly,
                    "sequence_flagged": sequence,
                }
            },
        )


def get_flag_status(record):
    flagged = False
    sequence = False
    assembly = False
    if "cleanData" in record:
        if (
            "Status" in record["cleanData"]
            and record["cleanData"]["Status"] == "Failed"
        ):
            flagged = True
        if (
            "Mean_Coverage_raw" in record["cleanData"]
            and float(record["cleanData"]["Mean_Coverage_raw"]) < 25
        ):
            assembly = True
        if (
            "HalfCov_Contig_Bases" in record["cleanData"]
            and "Bases_In_Contigs" in record["cleanData"]
        ):
            halfcov_bases = float(record["cleanData"]["HalfCov_Contig_Bases"])
            contig_bases = float(record["cleanData"]["Bases_In_Contigs"])
            raw_bases = float(record["cleanData"]["Bases_In_Contigs_raw"])
            if halfcov_bases / contig_bases > 1:
                sequence = True
            elif (raw_bases - contig_bases) / contig_bases > 5:
                sequence = True
    return flagged, sequence, assembly


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or len(args) == 0:
        sys.exit("Must give an identifier")
    elif len(args) == 1:
        mongo_server = "ncbs-dev-09.biotech.cdc.gov"
    else:
        mongo_server = args[0]
        client = MongoClient(
            mongo_server,
            27017,
            username="bmgap-writer",
            password="bmgap-example",
            authSource="BMGAP",
        )
        db = client.BMGAP
        main(args[1], db)

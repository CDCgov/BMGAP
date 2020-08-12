#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Title: insert_new_sample.py
Description:
Usage:
Date Created: 2018-10-29 11:17
Last Modified: Thu 02 Jul 2020 01:05:03 PM EDT
Author: Reagan Kelly (ylb9@cdc.gov)
"""

import re
import os
import argparse
from pymongo import MongoClient


def main(identifier, db_host, count, submitter, reads):
    mongo_host = db_host
    identifier = identifier
    source_path = reads
    fwd_read = get_fastq_file(source_path) if source_path else None
    client = MongoClient(
        mongo_host,
        27017,
        username="bmgap-writer",
        password="bmgap-example",
        authSource="BMGAP",
    )
    db = client.BMGAP
    insert_statement = {
        "identifier": identifier,
        "count": count,
        "Submitter": submitter,
    }
    if fwd_read:
        insert_statement["fwdReadPath"] = os.path.join(source_path, fwd_read)
    res = db.internal.insert_one(insert_statement)
    print(res.inserted_id)


def get_fastq_file(path):
    if (
        re.search("instruments", path)
        or re.search("bmgap-pipeline-testing", path)
        or re.search("data/DTT", path)
    ):
        # If the data comes from BML remove the sample subdirectory from the fastq path
        fastq_path_raw = path.split("/")
        fastq_path_parts = [x for x in fastq_path_raw if x != ""]
        fastq_path = os.path.join(*fastq_path_parts[:-1])
        contents = os.listdir(os.path.join("/" + fastq_path))
    else:
        contents = os.listdir(path)
    for obj in contents:
        if re.search(".*R1_001.fastq.gz", str(obj)):
            return obj
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Identifier
    parser.add_argument("-i", "--identifier", action="store", required=True)
    # Database
    parser.add_argument("-d", "--db_host", action="store", required=True)
    # Count
    parser.add_argument("-c", "--count", action="store", required=False, default=1)
    # Submitter
    parser.add_argument(
        "-s", "--submitter", action="store", required=False, default="BML"
    )
    # Path
    parser.add_argument("-r", "--reads", action="store", required=False, default=None)

    args = vars(parser.parse_args())
    main(**args)

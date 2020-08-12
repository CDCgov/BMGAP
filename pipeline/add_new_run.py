#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
#

"""
Title: add_new_run.py
Description:
Usage:
Date Created: 2019-02-11 17:42
Last Modified: Mon 07 Oct 2019 06:09:43 PM EDT
Author: Reagan Kelly (ylb9@cdc.gov)
Last Modified: Jun 12 2020 by Xiaoyu Zheng (qiu5@cdc.gov)
Changes: Added samples_running field in runs to reveal number of runs that are running for a run
"""

import argparse
import datetime
from pymongo import MongoClient


def main(run, count, submitter, db_host):
    dateval = datetime.datetime.now()
    run_parts = run.split("_")
    sequencer = run_parts[1] if len(run_parts) > 1 else None
    mongo_host = db_host
    client = MongoClient(
        mongo_host,
        27017,
        username="bmgap-writer",
        password="bmgap-example",
        authSource="BMGAP",
    )
    db = client.BMGAP
    run_exists = True if db.runs.count_documents({"run": run}) > 0 else False
    run_tracker_exists = (
        True if db.active_runs.count_documents({"run": run}) > 0 else False
    )
    if not run_exists:
        insert_statement = {
            "run": run,
            "samples": int(count),
            "sequencer": sequencer,
            "submitter": submitter,
            "date": dateval,
            "analysis_running": True,
            "samples_running": int(count),
        }
        db.runs.insert_one(insert_statement)
    if not run_tracker_exists:
        active_run_statement = {"Run_ID": run, "Samples": []}
        db.active_runs.insert_one(active_run_statement)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # database
    parser.add_argument("-d", "--db_host", action="store", required=True)

    # count
    parser.add_argument("-c", "--count", action="store", required=False, default=1)

    # Path
    parser.add_argument("-r", "--run", action="store", required=True, default=None)

    # submitter
    parser.add_argument(
        "-s", "--submitter", action="store", required=True, default=None
    )

    args = vars(parser.parse_args())
    main(**args)

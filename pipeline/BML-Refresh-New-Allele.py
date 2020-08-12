#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient
import sys
import subprocess


if __name__ == "__main__":
    rerunning_script = (
        "./pipeline/BML-Internal-ReRunner.sh"
    )
    pipeline_folder = "./pipeline"
    if len(sys.argv) == 1:
        mongo_server_name = "bmgap-poc.biotech.cdc.gov"
    else:
        mongo_server_name = sys.argv[1]
    mongo_server = "mongodb://" + mongo_server_name
    client = MongoClient(
        mongo_server, username="bmgap-writer", password="bmgap-example", authSource="BMGAP"
    )
    db = client.BMGAP
    query = db.internal.find(
        {"$or": [{"MLST.Nm_MLST_ST": "New"}, {"MLST.Hi_MLST_ST": "New"}]},
        {"_id": 0, "location": 1},
    )
    for record in query:
        if "location" in record:
            command = " ".join(
                ["qsub", rerunning_script, pipeline_folder, mongo_server_name, "Locus"]
            )
            subprocess.call([command], cwd=record["location"], shell=True)

#!/usr/bin/env python3.4
### Species Analysis Tool v1
### Import Modules ###
import sys
from Bio import SeqIO
import os
import string
import re
import operator
import csv
import pprint as pp
import locale
import argparse
import datetime
import json
import time
import shutil
from multiprocessing import Pool,Process, Queue
import tempfile
import sqlite3
from random import randint
from subprocess import *
encoding = locale.getdefaultlocale()[1]
if not encoding:
    encoding = 'UTF-8'

##PATHS###
SCRIPT_PATH = os.path.realpath(__file__)
DIR_PATH = os.path.dirname(os.path.dirname(SCRIPT_PATH))
MASH_DB = os.path.join(DIR_PATH,"lib","species_db_v1_2.msh")
REFSEQ_DB = os.path.join(DIR_PATH,"lib","RefSeqSketchesDefaults.msh")
#REFSEQ_DB = os.path.join(DIR_PATH,"lib","refseq_collection.msh")
BLAST_DB = os.path.join(DIR_PATH,"lib","blast_db","species_db_main")
SQLITE_DB = os.path.join(DIR_PATH,"sqlite3_db","species_db_v1_2")
conn = sqlite3.connect(SQLITE_DB)
c = conn.cursor()
OUTPUT_DIR = ""
VERBOSITY = False


def set_output(output):
	global OUTPUT_DIR
	OUTPUT_DIR = output
	if os.path.isdir(output):
		print("Output Directory",output,"aleady exists, not creating")
	else:
		os.system("mkdir {}".format(output))
		print("Created Output Directory",output)
		
def set_verbosity():
	global VERBOSITY
	VERBOSITY = True


def create_json(data,thresholds):
	pre_json = data
	for lab_id in data:
		if lab_id not in pre_json:
			pre_json[lab_id] = {"mash_results":{}}
		over_threshold = data[lab_id]["mash_results"]["Above_Threshold"]
		if not over_threshold:
			notes = "No hit above threshold from reference collection - Reporting Top RefSeq Hit"			
			mash_hit = data[lab_id]["mash_results"]["Top Match"]
			mash_pval = data[lab_id]["mash_results"][mash_hit]["p_val"]
			mash_hash = data[lab_id]["mash_results"][mash_hit]["hash"]
			mash_score = data[lab_id]["mash_results"][mash_hit]["score"]
			mash_species = mash_hit
			mash_source = "ncbi_refseq"
		else:
			if len(over_threshold) == 1:
				notes = "Hit above threshold"				
				for organism in over_threshold:
					mash_species = organism
					mash_hit = over_threshold[organism]["hit"]
					mash_pval = over_threshold[organism]["p_val"]
					mash_hash = over_threshold[organism]["hash"]
					mash_score = over_threshold[organism]["score"]
					mash_source = over_threshold[organism]["source"]							
			elif len(over_threshold) > 1:	
				notes = "multiple species above threshold -"				
				current_highest_score = 0.0
				i=1
				for organism in over_threshold:
					notes+= "{}. {} with score {}% to hit {} ".format(str(i),organism, str(over_threshold[organism]["score"]),str(over_threshold[organism]["hit"]))
					i+=1
					if over_threshold[organism]["score"] > current_highest_score:
						mash_species = organism
						current_highest_score = over_threshold[organism]["score"]
						mash_score = current_highest_score	
				mash_pval =  over_threshold[mash_species]["p_val"]
				mash_hit =  over_threshold[mash_species]["hit"]
				mash_hash =  over_threshold[mash_species]["hash"]
				mash_source =  over_threshold[mash_species]["source"]	
		mash_species_list = mash_species.split("_")
		if len(mash_species_list) > 1:
			mash_species = string.capwords(mash_species_list[0]) + " " + mash_species_list[1]
		else:
			mash_species = string.capwords(mash_species_list[0])							

		pre_json[lab_id]["mash_results"] = {"species":mash_species,"top_hit":mash_hit,"mash_pval":mash_pval,"mash_hash":mash_hash,"score":mash_score,"source":mash_source,"notes":notes}
	with open(os.path.join(OUTPUT_DIR,"species_analysis_{}.json".format(time.time())),"w") as f:
		json.dump(pre_json,f)
	return pre_json
				
def output_files_2(format,output,data,thresholds):
	if format == "csv":
		with open("{}/species_analysis_{}.csv".format(OUTPUT_DIR,time.time()),"w") as csvfile:
			csvwrite = csv.writer(csvfile,delimiter=',',quotechar='|',quoting= csv.QUOTE_MINIMAL)
			csvwrite.writerow(["Lab_ID","Top_Species","Notes","1-Mash Dist","Mash_P_value","Mash_Hash","Mash_Entry","Mash_Entry_Source"])
			for lab_id in data:
				mash_species = data[lab_id]["mash_results"]["species"]
				notes = data[lab_id]["mash_results"]["notes"]
				mash_score = data[lab_id]["mash_results"]["score"]
				mash_pval = data[lab_id]["mash_results"]["mash_pval"]
				mash_hash = data[lab_id]["mash_results"]["mash_hash"]
				mash_hit = data[lab_id]["mash_results"]["top_hit"]
				mash_source = data[lab_id]["mash_results"]["source"]
				csvwrite.writerow([lab_id,mash_species,notes,mash_score,mash_pval,mash_hash,mash_hit,mash_source])		
		
def output_files(format,output,data,thresholds):	
	if format == "csv":
		with open("{}/species_analysis_{}.csv".format(OUTPUT_DIR,time.time()),"w") as csvfile:
			csvwrite = csv.writer(csvfile,delimiter=',',quotechar='|',quoting= csv.QUOTE_MINIMAL)
			csvwrite.writerow(["Lab_ID","Top_Species","Notes","1-Mash Dist","Mash_P_value","Mash_Hash","Mash_Entry","Mash_Entry_Source"])
			for lab_id in data:
				multiple = False
				print(lab_id)					
				over_threshold = data[lab_id]["mash_results"]["Above_Threshold"]			
				if over_threshold:
					if len(over_threshold) == 1:
						for organism in over_threshold:
							mash_pval = over_threshold[organism]["p_val"]
							mash_hash = over_threshold[organism]["hash"]
							mash_score = over_threshold[organism]["score"]
							mash_hit = over_threshold[organism]["hit"]
					elif len(over_threshold) > 1:
						multiple = True
				else:
					mash_hit = data[lab_id]["mash_results"]["Top Match"]
					mash_score = data[lab_id]["mash_results"][mash_hit]["score"]
				
				if not multiple:
					if mash_hit in thresholds:
						genus = thresholds[mash_hit]["genus"]
						species = thresholds[mash_hit]["species"]
						source = thresholds[mash_hit]["source"]
						mash_species = genus+"_"+species
						notes = "Hit above threshold"
						mash_source = source
					else:
						notes = "No hit above threshold from reference collection - Reporting Top RefSeq Hit"
						mash_species = mash_hit
						mash_source = "ncbi_refseq"
						mash_pval = data[lab_id]["mash_results"][mash_hit]["p_val"]						
						mash_hash = data[lab_id]["mash_results"][mash_hit]["hash"]						
				else:
					mash_species_list = []
					mash_sources_list = []
					mash_pval_list = []
					mash_score_list = []
					mash_source_list = []
					mash_hash_list = []
					mash_hit_list = []
					notes = "multiple species above threshold -"
					current_highest_score = 0.0
					i=1
					for organism in over_threshold:
						notes+= "{}. {} with score {}% to hit {} ".format(str(i),organism, str(over_threshold[organism]["score"]),str(over_threshold[organism]["hit"]))
						i+=1
						if over_threshold[organism]["score"] > current_highest_score:
							mash_species = organism
							current_highest_score = over_threshold[organism]["score"]
							mash_score = current_highest_score
						
					mash_pval =  over_threshold[mash_species]["p_val"]
					mash_hit =  over_threshold[mash_species]["hit"]
					mash_hash =  over_threshold[mash_species]["hash"]
					mash_source =  over_threshold[mash_species]["source"]
			
				csvwrite.writerow([lab_id,mash_species,notes,mash_score,mash_pval,mash_hash,mash_hit,mash_source])		

def mash_sketch_refseq(threads,redo,temp_dir):
	print("Scanning low-scoring queries against RefSeq")
	for lab_id in redo:
		file_path = redo[lab_id] 
		call(["cp","{}".format(file_path),"{}/".format(temp_dir)],shell=False)
	threads = threads
	kmer_size = 21
	sketch_size = 1000
	sketch_info_dict = {}
	call(["mash sketch -k {} -p {} -s {} -o {} {}".format(kmer_size,threads,sketch_size,os.path.join(temp_dir,"sp_ref_sketch"),os.path.join(temp_dir,"*.f*"))], shell=True)
	sketch_info_dict["path"] = temp_dir+"/sp_ref_sketch.msh"	
	return sketch_info_dict
	

def parse_results(results,input_file,thresholds):
	redo = {}
	for lab_id in results:
		path = os.path.join(input_file,lab_id)
		over_threshold = results[lab_id]["mash_results"]["Above_Threshold"]
		if not over_threshold:
			print(lab_id,"has no scores over thresholds")
			redo[lab_id] = path
			continue
	return redo


		
	
def mash_dist(sketch,mash_db_name,threads,refseq,thresholds):
	start_time = time.time()
	print("Calculating Distances")
	mash_results_dict = {}
	mash_results = check_output(["mash","dist","-p",threads,mash_db_name,sketch],shell=False)
	dist_time = time.time()
	print("Distances calculated in {} seconds, parsing data".format(dist_time-start_time))
	mash_result = re.split(b"\n",mash_results.rstrip())				
	for line in mash_result:
		if refseq:
			hit = line.decode(encoding).split("\t")[0].split("-")[-1].split(".fna")[0]
		else:
			hit = line.decode(encoding).split("\t")[0]
		query_name = line.decode(encoding).split("\t")[1]
		query_name = os.path.basename(query_name)
		if not query_name in mash_results_dict:
			mash_results_dict[query_name] = {"mash_results":{}}
		mash_dist = float(line.decode(encoding).split("\t")[2])
		p_val = line.decode(encoding).split("\t")[3]
		match_hash = line.decode(encoding).split("\t")[4]
		mash_score = (1-mash_dist)
		mash_results_dict[query_name]["mash_results"][hit] = {"score":mash_score,"p_val":p_val,"hash":match_hash,"hit":hit}
	print("Data parsed in {} seconds, sorting and finding top hits".format(time.time()-dist_time))
	for query in mash_results_dict:
		over_threshold = {}
		mash_results_dict[query]["mash_results"]["Above_Threshold"] = {}		
		current_mash_hit = "N/A"
		current_mash_score = 0
		for hit in mash_results_dict[query]["mash_results"]:
			if hit != "Above_Threshold":
				if not refseq:
					score = mash_results_dict[query]["mash_results"][hit]["score"]	
					threshold = thresholds[hit]["threshold"]										
					if score >= threshold:				
						species = thresholds[hit]["species"]
						p_val = mash_results_dict[query]["mash_results"][hit]["p_val"]
						hash_val = mash_results_dict[query]["mash_results"][hit]["hash"]
						hit_name = mash_results_dict[query]["mash_results"][hit]["hit"]
						source = thresholds[hit]["source"]							
						genus = thresholds[hit]["genus"]
						organism = genus+"_"+species
						if organism not in over_threshold:
							over_threshold[organism] = {"score":score,"p_val":p_val,"hash":hash_val,"hit":hit_name,"source":source}
						else:
							current_score = over_threshold[organism]["score"]
							if score > current_score:
								over_threshold[organism] = {"score":score,"p_val":p_val,"hash":hash_val,"hit":hit_name,"source":source}		
					
				else:
					if mash_results_dict[query]["mash_results"][hit]["score"] > current_mash_score:
						current_mash_score = mash_results_dict[query]["mash_results"][hit]["score"]
						current_mash_hit = hit
		
		if refseq:
			mash_results_dict[query]["mash_results"]["Top Match"] = current_mash_hit
		else:
			mash_results_dict[query]["mash_results"]["Above_Threshold"] = over_threshold
			
	return mash_results_dict
	
def mash_sketch(threads,input_file,temp_dir,sketch_info):
	print("Running Mash")
	threads = threads
	kmer_size = 21
	sketch_size = 1000
	sketch_info_dict = {}
	call(["mash sketch -k {} -p {} -s {} -o {} {}".format(kmer_size,threads,sketch_size,os.path.join(temp_dir,"sp_sketch"),os.path.join(input_file,"*.f*"))], shell=True)
	sketch_info_dict["path"] = temp_dir+"/sp_sketch.msh"
	sketch_info = {"sketch_dict":sketch_info_dict,"temp_dir":temp_dir}
	return sketch_info

def main():
	### Main Arg Parse ###
	parser = argparse.ArgumentParser(description="Script for quickly determining species")
	parser.add_argument('-d','--indir',help="Input Directory: Directory of FASTA files to analyze")
	parser.add_argument('-f','--file',help="Tab-delimited input containing Name and File Path (Name \t Filepath)")
	parser.add_argument('-v','--verbose',help="verbose standard output (default = false)", action="store_true")
	parser.add_argument('-o','--out',help="Output File name", required=True)
	parser.add_argument('-j','--json',help="Only output json file (default = false)", action="store_true")
	parser.add_argument('-t','--threads',help="Number of max threads to use (default=1)",default="1")
	args = vars(parser.parse_args())
	start_time = time.time()
	
	### Print Args ###
	print ("Running with the following parameters:")
	for arg in args:
		print (arg,":",args[arg])
		
	### Set Output (Create if doesn't exist already) ###
	set_output(args["out"])
	if args["verbose"]:
		set_verbosity()
		
	### Initialize variables ###
	q_dict = {}
	sketches_dict = {}
	sketches = []
	sketch_info = {}
	results_dict = {}
	thresholds = {}

	c.execute("select g.filepath,o.threshold,o.species,o.genus,s.source_location from Genome g, Organism o, Source s where g.organism_id=o.organism_id and s.source_id=g.source_id")
	org_results = c.fetchall()
	for org_id in org_results:
		file_path = org_id[0]
		threshold = org_id[1]
		species = org_id[2]
		genus = org_id[3]
		source = org_id[4]
		if file_path not in thresholds:
			thresholds[file_path] = {"threshold":threshold,"species":species,"genus":genus,"source":source}
	
	temp_dir = tempfile.mkdtemp()
	
	### If input is given as a file containing tab delimited name and file path ###
	if args["file"]:
		print("Arranging input files for sketching")
		### Copy input files to a temp directory for quality assurance ###
		with open(args["file"]) as f:
			indir_text = f.readlines()
		for line in indir_text:
			q_name = line.split('\t')[0]
			q_path = line.split('\t')[1]
			call(["cp","{}".format(q_path.replace("\n","")),"{}/".format(temp_dir)],shell=False)
		### Create MASH sketches and get path for temp directory containing sketch compilation ###	
		sketch_creation = mash_sketch(args["threads"],temp_dir,temp_dir,sketch_info)
		sketch_path = sketch_creation["sketch_dict"]
		working_dir = temp_dir
		
	### If input is given as a directory containing FASTA files ###	 
	elif args["indir"]:
		### Create MASH sketches and get temp directory containing sketch compilation ###
		sketch_creation = mash_sketch(args["threads"],args["indir"],temp_dir,sketch_info)
		sketch_path = sketch_creation["sketch_dict"]
		working_dir = args["indir"]
	### Calculate MASH distances, then parse distances to see if they are below threshold ###
	mash_results = mash_dist(sketch_path["path"],MASH_DB,args["threads"],False,thresholds)
	redo_set = parse_results(mash_results,working_dir,thresholds)
	### If below threshold, redo mash distance comparisons against REFSEQ ###
	if redo_set:
		redo_sketch = mash_sketch_refseq(args["threads"],redo_set,temp_dir)
		redo_results = mash_dist(redo_sketch["path"],REFSEQ_DB,args["threads"],True,thresholds)
		for query in redo_results:
			mash_results[query]["mash_results"] = redo_results[query]["mash_results"]
	
	### Create JSON output ###		
	final_results = create_json(mash_results,thresholds)
	
	### Create Output csv file ###
	if not args["json"]:
		output_files_2("csv",args["out"],final_results,thresholds)
	shutil.rmtree(temp_dir)
	print("Species results determined for all queries in {} seconds".format(str(time.time()-start_time)))
if __name__ == "__main__":
	main()

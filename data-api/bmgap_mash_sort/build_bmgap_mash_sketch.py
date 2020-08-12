#!/usr/bin/env python3.4
### Get closest hits
### Import Modules ###

import sys
import argparse
import locale
import os
import re
import urllib3
import json
import math
from collections import OrderedDict
from operator import itemgetter
import pprint as pp
from Bio import SeqIO
from subprocess import *
from time import sleep
import tempfile
encoding = locale.getdefaultlocale()[1]
OUTPUT_DIR = ""
http = urllib3.PoolManager()
def set_output(output):
	global OUTPUT_DIR
	OUTPUT_DIR = output
	if os.path.isdir(output):
		print("Output Directory",output,"aleady exists, not creating")
	else:
		os.system("mkdir {}".format(output))
		print("Created Output Directory",output)


def call_bmgap_api():
	final_data = {} #set up dict to hold our final data
	#since there is no direct way to filter by run using the API yet, we will use a different approach
	#we will pull all of the data from BMGAP, and then filter it ourselves by the run that we want
	#since there is no way to pull all of the data from BMGAP, we will do one API call with default settings to get the count the total # of records, then another to pull all of those records
	url_1 = 'http://amdportal-sams.cdc.gov/bmgap-api/samples' #first url
	#this is the actual API request below. REST APIs usually have two options (GET and POST). GET is when we want to get data, POST is when we want to submit data. Either one can also return data.
	request = http.request("GET",url_1) #request is a httpresponse object, we want the data stored in it, and we want to decode it from bytes to utf-8 unicode
	
	request_data = json.loads(request.data.decode('utf-8')) #this handles the decoding, and it converts the json to a python dictionary "request_data"
	total_records = request_data["total"] #get total record count
	pages = math.ceil(total_records/1000)
	print("grabbing {} BMGAP records across {} pages".format(total_records,pages)) #print how many records we will get in the next API call
	merged_data = []
	for i in range(1,pages+1):
		print("getting page {}".format(i))
		url_2 = 'http://amdportal-sams.cdc.gov/bmgap-api/samples?page={}&perPage={}'.format(i,1000) #Now that we know how many records exist, we will pull them all by adding the perPage filter
		request = http.request("GET",url_2)
		request_data = json.loads(request.data.decode('utf-8')) #override our previous request_data with the total records
		merged_data.append(request_data["docs"])
	total = 0
	for obj in merged_data:
		for record in obj:
			total+=1		
	print("got {} BMGAP records".format(total)) #make sure we got them all by printing the count of the records
	for obj in merged_data:
		for record in obj:
			if "mash" in record:
				if "QC_flagged" in record: #if the record has been QC flagged
					if record["QC_flagged"]: #true means it was flagged as bad quality
						continue #skip
					else:
						if "assemblyPath" in record:
							assembly_path = record["assemblyPath"]
						else:
							continue
						lab_id = record["Lab_ID"]
						bmgap_id = record["identifier"]
						assembly_file = assembly_path.split("/")[-1]						
						final_data[bmgap_id] = {"lab_id":lab_id,"assembly_path":assembly_path,"assembly_file":assembly_file}

	return final_data		


def mash_sketch_list(threads,mash_assembly_list,output_dir,temp_dir):
	print("Running Mash")
	kmer_size = 32
	sketch_size = 10000
	with open(os.path.join(temp_dir,"temp_assembly_list"),"w") as f:
		for obj in mash_assembly_list:
			f.write("{}\n".format(obj))
	mash_assembly_list = os.path.join(temp_dir,"temp_assembly_list")
	out_sketch_name = "BMGAP_DATA_MASH_DB"
	output_sketch = os.path.join(output_dir,out_sketch_name)
	call(["mash sketch -k {} -p {} -l {} -s {} -o {}".format(kmer_size,threads,mash_assembly_list,sketch_size,output_sketch)], shell=True)
	call(["rm {}".format(mash_assembly_list)], shell=True)
	return("{}.msh".format(output_sketch))



def main():
	parser = argparse.ArgumentParser(description="Build BMGAP mash sketch")
	parser.add_argument('-o','--out',help="Location of output", required=True)
	parser.add_argument('-t','--threads',help="Number of threads to use (default=1)", default="1")
	args = vars(parser.parse_args())
	threads = args["threads"]
	set_output(args["out"])
	
	
	mash_assembly_list = []
	temp_dir = tempfile.mkdtemp()
	#gets all data in BMGAP
	bmgap_data = call_bmgap_api()
	for record in bmgap_data:
		mash_assembly_list.append(bmgap_data[record]["assembly_path"])	
		
	#sketches assemblies
	mash_db = mash_sketch_list(threads,mash_assembly_list,OUTPUT_DIR,temp_dir)
	print("created {}".format(mash_db))


if __name__ == "__main__":
	main()

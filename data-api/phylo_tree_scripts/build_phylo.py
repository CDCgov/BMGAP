#!/usr/bin/env python3.4
### Phylogeny Building Tool v1
### Import Modules ###
import sys
from Bio import SeqIO
from Bio.Phylo.TreeConstruction import DistanceCalculator
from Bio.Phylo.TreeConstruction import _DistanceMatrix
from Bio.Phylo.TreeConstruction import DistanceTreeConstructor
from Bio import Phylo
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
import math
import collections
import urllib3
from multiprocessing import Pool,Process, Queue
import tempfile
import sqlite3
from random import randint
from subprocess import *
from scipy import stats
import numpy as np
from operator import attrgetter


#import matplotlib.pyplot as plt
encoding = locale.getdefaultlocale()[1]
http = urllib3.PoolManager()
##PATHS###
SCRIPT_PATH = os.path.realpath(__file__)
DIR_PATH = os.path.dirname(SCRIPT_PATH)
home_dir = os.path.expanduser("~")
mask_map_script = "{}/ML/tools/mask_mapped_aln/mask_mapped_aln.py".format(home_dir)
adjust_size_script = "{}/ML/tools/mask_mapped_aln/adjust_partition_size.py".format(home_dir)
pacbio_ref_sketch = "{}/ML/Projects/NadavTopaz/Scripts/lib/pacbio_references.msh".format(home_dir)
reference_files = "{}/ML/Projects/NadavTopaz/Scripts/reference_pacbios".format(home_dir)
#GENOME_DIR = "{}/ML/Projects/NadavTopaz/All_nm/fastas".format(home_dir)
# print(home_dir)
# print(mask_map_script)
# print(GENOME_DIR)
# print(adjust_size_script)
OUTPUT_DIR = ""
VERBOSITY = False
weights = {"1":1.0,
			"2":0,
			"3":0}
fasta_extensions = [".fa",".fasta",".fna"]
def set_output(output):
	global OUTPUT_DIR
	OUTPUT_DIR = output
	if os.path.isdir(output):
		print("Output Directory",output,"aleady exists, not creating")
	else:
		os.system("mkdir {}".format(output))
		print("Created Output Directory",output)
def pick_reference(query_sketch,threads):
	mash_results = check_output(["mash","dist","-p",threads,pacbio_ref_sketch,query_sketch],shell=False)
	mash_result = re.split(b"\n",mash_results.rstrip())
	current_min = 100.0
	current_ref = ""
	for line in mash_result:
		line = line.decode(encoding)
		ref_assembly = line.split("\t")[0]
		query_name = line.split("\t")[1]
		mash_dist = float(line.split("\t")[2])
		if mash_dist < current_min:
			current_min = mash_dist
			current_ref = ref_assembly
	ref_path = os.path.join(reference_files,current_ref)
	return ref_path
	
def pick_genomes(query_sketch,mash_db,threads,max_num,force_max):
	print("Calculating Distances")
	mash_results_dict = {}
	mash_results = check_output(["mash","dist","-p",threads,mash_db,query_sketch],shell=False)
	mash_result = re.split(b"\n",mash_results.rstrip())	
	seen_basenames = []
	counts = {}
	for line in mash_result:
		query_name = line.decode(encoding).split("\t")[1]
		query_name = os.path.basename(query_name)
		if query_name not in mash_results_dict:
			mash_results_dict[query_name] = {"mash_results":{},"mash_dists":[]}		
		hit = line.decode(encoding).split("\t")[0]
		if "/" in hit:
			hit_path = hit
			hit = os.path.basename(hit)			
		if "_" in hit:
			hit_basename = hit.split("_")[0]
		else:
			hit_basename = hit
		if "_" in query_name:
			query_basename = query_name.split("_")[0]
		if query_basename == hit_basename:
			continue
		if query_name == hit:
			continue
		mash_dist = float(line.decode(encoding).split("\t")[2])
		p_val = line.decode(encoding).split("\t")[3]
		match_hash = line.decode(encoding).split("\t")[4]
		mash_score = mash_dist
		mash_results_dict[query_name]["mash_results"][hit] = {"score":mash_score,"p_val":p_val,"hash":match_hash,"hit":hit,"path":hit_path}
		mash_results_dict[query_name]["mash_dists"].append(mash_score)

	final_genomes = {"all_genomes":[],"details":{}}
	for query in mash_results_dict:
		scores_set = []	
		for hit,_ in sorted(mash_results_dict[query]["mash_results"].items(),key=lambda x: float(x[1]["score"])):
			score = mash_results_dict[query]["mash_results"][hit]["score"]
			if score not in scores_set:
				scores_set.append(score)
				
		a = np.asarray(scores_set)
		count = 0
		for hit,_ in sorted(mash_results_dict[query]["mash_results"].items(),key=lambda x: float(x[1]["score"])):
			if hit not in final_genomes["all_genomes"]:
				score = mash_results_dict[query]["mash_results"][hit]["score"]	
				if count < max_num:
					hit_path = mash_results_dict[query]["mash_results"][hit]["path"]
					final_genomes["all_genomes"].append(hit_path)
					final_genomes["details"][hit] = {"query":query,"dist":score}
					count+=1
	
	print(final_genomes["all_genomes"])
	print(len(final_genomes["all_genomes"]))
	final_scores = []
	for query in mash_results_dict:	
		for genome in final_genomes["details"]:
			score = mash_results_dict[query]["mash_results"][genome]["score"]
			final_scores.append(score)
			#print(genome,score)
	#print(sorted(final_scores))	
	#~ plt.savefig("hist.svg",format="svg")
	#final_genomes["query"] = query_name
	return final_genomes
	
def mash_sketch(threads,genome_dir,temp_dir,sketch_info):
	print("Running Mash")
	threads = threads
	kmer_size = 32
	sketch_size = 10000
	sketch_info_dict = {}
	call(["mash sketch -k {} -p {} -s {} -o {} {}/*".format(kmer_size,threads,sketch_size,os.path.join(temp_dir,"nm_sketch"),genome_dir)], shell=True)
	sketch_info_dict["path"] = temp_dir+"/nm_sketch.msh"
	sketch_info = {"sketch_dict":sketch_info_dict,"temp_dir":temp_dir}
	return sketch_info

def mash_sketch_list(threads,mash_assembly_list,output_dir,proj_name,temp_dir):
	print("Running Mash")
	kmer_size = 32
	sketch_size = 10000
	with open(os.path.join(temp_dir,"temp_assembly_list"),"w") as f:
		for obj in mash_assembly_list:
			f.write("{}\n".format(obj))
	mash_assembly_list = os.path.join(temp_dir,"temp_assembly_list")
	unique_time = str(time.time()).split(".")[1]
	out_sketch_name = "{}_{}".format("BMGAP_DATA_MASH_DB",unique_time)
	output_sketch = os.path.join(output_dir,out_sketch_name)
	call(["mash sketch -k {} -p {} -l {} -s {} -o {}".format(kmer_size,threads,mash_assembly_list,sketch_size,output_sketch)], shell=True)
	call(["rm {}".format(mash_assembly_list)], shell=True)
	return("{}.msh".format(output_sketch))
	
def make_mash_matrix(threads,genome_list,output_dir,proj_name,temp_dir):
	print("Running Mash")
	kmer_size = 32
	sketch_size = 10000
	with open(os.path.join(temp_dir,"temp_assembly_list"),"w") as f:
		for obj in genome_list:
			f.write("{}\n".format(obj))	
	mash_assembly_list = os.path.join(temp_dir,"temp_assembly_list")
	unique_time = str(time.time()).split(".")[1]
	out_sketch_name = "{}_{}".format(proj_name,unique_time)
	output_sketch = os.path.join(output_dir,out_sketch_name)
	call(["mash sketch -k {} -p {} -l {} -s {} -o {}".format(kmer_size,threads,mash_assembly_list,sketch_size,output_sketch)], shell=True)
	call(["rm {}".format(mash_assembly_list)], shell=True)
	output_sketch = "{}.msh".format(output_sketch)
	mash_results = check_output(["mash","dist","-p",threads,output_sketch,output_sketch],shell=False)
	mash_result = re.split(b"\n",mash_results.rstrip())
	headers = []
	data_set = {}
	for line in mash_result:
		line = line.decode(encoding)
		query = line.split("\t")[0]
		query = os.path.basename(query)
		query = query.split(".")[0]
		subject = line.split("\t")[1]
		subject = os.path.basename(subject)
		subject = subject.split(".")[0]
		score = float(line.split("\t")[2])
		if query not in data_set:
			data_set[query] = {}
		if subject not in data_set[query]:
			data_set[query][subject] = score
		if query not in headers:
			headers.append(query)
	i=0
	final_text="\t"
	header_dict={}
	for query in sorted(headers):
		header_dict[i] = query
		i+=1
		final_text+="{}\t".format(query)
	final_text+="\n"
	final_text.replace("\t\n","\n")
	for query in sorted(data_set):
		final_text+="{}\t".format(query)
		for i in range(0,len(headers)):
			current_score = data_set[query][header_dict[i]]
			final_text+="{}\t".format(current_score)
		final_text+="\n"
		final_text.replace("\t\n","\n")
	return(final_text)

	

def call_snippy(ref,file_path):
	entry = file_path.split("/")[-1]
	if ".fasta" in entry:
		entry_name = entry.replace(".fasta","")
	else:
		entry_name = entry
	if "_" in entry_name:
		entry_name = entry_name.split("_")[0]
	call(["snippy","--outdir",os.path.join(OUTPUT_DIR,"snippy_dir","{}".format(entry_name)),"--cpus","1","--ref",ref,"--ctgs",file_path,"--force"],shell=False)
	#call(["snippy","--outdir",os.path.join(OUTPUT_DIR,"snippy_dir","{}".format(entry_name)),"--cpus","1","--ref",ref,"--ctgs",file_path],shell=False)
	return True

def snippy_check(snippy_dir):
	total_size = 0.0
	i=0
	size_dict = {}
	redo_list = []
	for snp_file in os.listdir(snippy_dir):
		file_path = os.path.join(snippy_dir,snp_file)
		size = os.stat(file_path).st_size
		total_size += float(size)
		i+=1
		size_dict[snp_file] = size
	avg_size = float(total_size/i)
	for obj in size_dict:
		if size_dict[obj] < avg_size:
			redo_list.append(obj)
	return redo_list
	
def run_snippy(final_genomes,threads,query_assemblies,dir_flag):
	processes = int(threads)
	pool = Pool(processes)
	snippy_dir = os.path.join(OUTPUT_DIR,"snippy_dir")
	snippy_list = []
	if os.path.isdir(snippy_dir):
		print("Snippy Directory",snippy_dir,"aleady exists, not creating")
	else:
		os.system("mkdir {}".format(snippy_dir))
		print("Created Output Directory",snippy_dir)
		
	for file_path in final_genomes["all_genomes"]:
		snippy_list.append(file_path)
	for file_path in query_assemblies:
		snippy_list.append(file_path)
	ref = final_genomes["ref"]
	snippy_time = [pool.apply_async(call_snippy,args=(ref,in_file)) for in_file in snippy_list]				
	output = [result.get() for result in snippy_time]
	
	pool.terminate()
	redo_list = snippy_check(snippy_dir)
	if len(redo_list) > 0:
		for obj in redo_list:
			for item in snippy_list:
				if obj in item:
					call_snippy(ref,item)	
	return snippy_dir

# def update_mash_sketch(mash_db,assembly_list):
	# mash_info_assemblies = {}
	# mash_info = check_output(["mash info {}".format(mash_db)],shell=True)
	# pp.pprint(mash_info)
	# mash_info = mash_info.decode(encoding)
	# mash_info_lines = mash_info.split("\n")
	# print(mash_info_lines)
	# for line in mash_info_lines:
		# print(line)
		# if line.strip() == "":
			# continue
		# else:
			# if "[Hashes]" in line:
				# continue
			# line = line.replace(" ","***")
			# line_items_pre = line.split("***")
			# line_items = []
			# for obj in line_items_pre:
				# if obj.strip() != "":
					# line_items.append(obj)
			# if len(line_items) == 4:
				# mash_info_assemblies[line_items[2]] = ""
	# pp.pprint(mash_info_assemblies)
	# check_set = []
	# for genome_file_path in assembly_list:
		# genome_file = genome_file_path.split("\\")[-1]
		# if genome_file not in mash_info_assemblies:
			# check_set.append(genome_file_path)
			
	# return(check_set)
		
		
# def paste_sketch(threads,mash_db,input_file,temp_dir):
	# print("Running Mash")
	# threads = threads
	# in_file_name = input_file.split("\\")[-1]
	# kmer_size = 32
	# sketch_size = 10000
	# call(["mash sketch -k {} -p {} -s {} -o {} {}".format(kmer_size,threads,sketch_size,os.path.join(temp_dir,"input_sketch.msh"),input_file)], shell=True)
	# sketch_path = os.path.join(temp_dir,"input_sketch.msh")
	# call(["mash paste {} {}".format(mash_db,sketch_path)],shell=True)
	# print("added {} to mash db".format(in_file_name))
	# call(["rm {}".format(os.path.join(temp_dir,"input_sketch.msh"))],shell=True)
	
def call_bmgap_api():
	final_data = {} #set up dict to hold our final data
	#since there is no direct way to filter by run using the API yet, we will use a different approach
	#we will pull all of the data from BMGAP, and then filter it ourselves by the run that we want
	#since there is no way to pull all of the data from BMGAP, we will do one API call with default settings to get the count the total # of records, then another to pull all of those records
	url_1 = 'http://amdportal-sams.cdc.gov/bmgap-api/samples' #first url
	#this is the actual API request below. REST APIs usually have two options (GET and POST). GET is when we want to get data, POST is when we want to submit data. Either one can also return data.
	request = http.request("GET",url_1) #request is a httpresponse object, we want the data stored in it, and we want to decode it from bytes to utf-8 unicode
	
	request_data = json.loads(request.data.decode('utf-8')) #this handles the decoding, and it converts the json to a python dictionary "request_data"
	#pp.pprint(request_data) #print the data we got
	
	#for category in request_data:
	#	print(category) 		#this shows us that there are three main categories in the data, "docs", "total" and "limit" - the docs store the record data, and total tells us how many records exist in BMGAP, limit is set to 50 by default
	total_records = request_data["total"] #get total record count
	pages = math.ceil(total_records/1000)
	#print(pages)
	print("grabbing {} BMGAP records across {} pages".format(total_records,pages)) #print how many records we will get in the next API call
	#print(type(total_records)) #make sure "total_records" is an integeter and not a string, and it is an int
	merged_data = []
	for i in range(1,pages+1):
		print("getting page {}".format(i))
		url_2 = 'http://amdportal-sams.cdc.gov/bmgap-api/samples?page={}&perPage={}'.format(i,1000) #Now that we know how many records exist, we will pull them all by adding the perPage filter
		request = http.request("GET",url_2)
		#pp.pprint(request.data.decode('utf-8')) 
		request_data = json.loads(request.data.decode('utf-8')) #override our previous request_data with the total records
		#for record in request_data["docs"]: #now that we know that we want to loop through docs, we do so here and print each record
		#	pp.pprint(record)
		merged_data.append(request_data["docs"])
		#time.sleep(60)
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
							#orig_assembly_file = assembly_path.split("/")[-1]
							#assembly_file = orig_assembly_file.replace("-","_")
							#assembly_path = os.path.join(assembly_path.replace(orig_assembly_file,""),assembly_file)
						else:
							continue
						lab_id = record["Lab_ID"]
						bmgap_id = record["identifier"]
						assembly_file = assembly_path.split("/")[-1]						
						final_data[bmgap_id] = {"lab_id":lab_id,"assembly_path":assembly_path,"assembly_file":assembly_file}

	#pp.pprint(final_data)
	#print(len(final_data))
	return final_data		

def error(error_dict):
	for error in error_dict:
		print(error_dict[error],error)
		exit()
		
def main():
	### Main Arg Parse ###
	parser = argparse.ArgumentParser(description="Automated Phylogeny Builder v1")
	parser.add_argument('-d','--indir',help="Input Directory: Directory of FASTA files to analyze")
	parser.add_argument('-o','--out',help="Output Directory", required=True)
	parser.add_argument('-t','--threads',help="Number of max threads to use (default=1)",default="1")
	parser.add_argument('-b','--mash_db',help="Provide prebuilt mash DB, otherwise build from scratch")
	parser.add_argument('-f','--fast',help="Fast option for distance based neighbor joining tree", action="store_true")
	parser.add_argument('-m','--max_num',help="Maximum number of isolates to include (default=50)",default="50")
	parser.add_argument('-g','--genomes',help="Provide genome directory to build tree with instead of automatically picking, requires -r flag")
	parser.add_argument('-r','--reference',help="Required with -g flag; provide reference to use for phylogeny when providing genome directory")
	parser.add_argument('-s','--snippy',help="existing snippy dir, requires -g and -r")
	parser.add_argument('-p','--proj_name',help="project prefix - will be used to label all files associated with project", required=True)
	args = vars(parser.parse_args())
	start_time = time.time()
	
	### Print Args ###
	print ("Running with the following parameters:")
	for arg in args:
		print (arg,":",args[arg])
		
	### Set Output (Create if doesn't exist already) ###
	set_output(args["out"])

		
	### Initialize variables ###
	automatic_selection = True
	threads = args["threads"]
	q_dict = {}
	sketches_dict = {}
	sketches = []
	sketch_info = {}
	results_dict = {}
	thresholds = {}
	error_dict = {}
	temp_dir = tempfile.mkdtemp()
	project_name = args["proj_name"]
	dir_flag = False
	mash_assembly_list = []
	max_num = int(args["max_num"])
	if args["fast"]:
		need_ref = False
	else:
		need_ref = True
	if args["mash_db"]:
		mash_db = args["mash_db"]
	if args["indir"]:
		input_dir = args["indir"]
	query_assemblies = []
	if args["snippy"]:
		if not args["genomes"]:
			error_dict["snippy dir provided without genome dir, exiting"] = "Input error: "
			error(error_dict)
		if not args["reference"]:
			error_dict["snippy dir provided without reference, exiting"] = "Input error: "
			error(error_dict)			
		automatic_selection = False
	if args["genomes"] and args["reference"]:
		input_dir = args["genomes"]
		reference = args["reference"]
		dir_flag = True
		automatic_selection = False
	if args["genomes"] and not args["reference"]:
		error_dict["Genome dir provided without reference, exiting"] = "Input error: "
		error(error_dict)
	if args["reference"] and not args["genomes"]:
		error_dict["Reference provided without genome directory, exiting"] = "Input error: "
		error(error_dict)
					
	
	in_file_counter = 0
	for in_file in os.listdir(input_dir):
		in_file_path = os.path.join(input_dir,in_file)
		query_assemblies.append(in_file_path)
		in_file_counter +=1
	max_num_per_query = (max_num-in_file_counter)/in_file_counter
	query_sketch = mash_sketch_list(threads,query_assemblies,OUTPUT_DIR,project_name,temp_dir)
	
	if need_ref:
		ref_path = pick_reference(query_sketch,threads)
	
	if not args["mash_db"]:
		bmgap_data = call_bmgap_api()
		for record in bmgap_data:
			mash_assembly_list.append(bmgap_data[record]["assembly_path"])	
		mash_db = mash_sketch_list(threads,mash_assembly_list,OUTPUT_DIR,project_name,temp_dir)
	
	if automatic_selection:
		final_genomes = pick_genomes(query_sketch,mash_db,args["threads"],int(max_num_per_query),force_max)
		if need_ref:
			final_genomes["ref"] = ref_path
			print(ref_path)
	else:
		final_genomes = {"all_genomes":[],"details":{},"ref":args["reference"]}
		for infile in os.listdir(args["genomes"]):
			for ext in fasta_extensions:
				if ext in infile:
					infile_path = os.path.join(args["genomes"],infile)
					if infile_path not in final_genomes["all_genomes"]:
						final_genomes["all_genomes"].append(infile_path)
						continue
	#pp.pprint(final_genomes)
	if not args["fast"]:
		if not args["snippy"]:
			snippy_dir = run_snippy(final_genomes,args["threads"],query_assemblies,dir_flag)
		else:
			snippy_dir = args["snippy"]
			redo_list = snippy_check(snippy_dir)
			for obj in redo_list:
				print(obj)
				for genome in os.listdir(input_dir):
					print(genome)
					if obj in genome:
						print("found")
						redo_obj = os.path.join(genome_dir,genome)
						call_snippy(reference,redo_obj)
						
						
		call(["snippy-core --prefix={}_core --aformat=fasta {}/*".format(project_name,snippy_dir)], shell=True)
		p2 = Popen(["mv {}_core* {}".format(project_name,snippy_dir)], shell=True)
		p2.wait()
		p3 = Popen(["python3 {} {}/{}_core.full.aln -o {}".format(mask_map_script,snippy_dir,project_name,OUTPUT_DIR)], shell=True)
		p3.wait()
		masked_aln_file = "{}/{}_core.full_masked.aln".format(OUTPUT_DIR,project_name)
		partition_file = "{}/{}_core.full_partition.txt".format(OUTPUT_DIR,project_name)
		print("gubbins")
		p4 = Popen(["run_gubbins.py -c {} -i 10 -u -p {}/gubbins_masked -v -t raxml {}".format(args["threads"],OUTPUT_DIR,masked_aln_file)], shell=True)
		p4.wait()
		gubbins_phylip_file = "{}/gubbins_masked.filtered_polymorphic_sites.phylip".format(OUTPUT_DIR)
		p5 = Popen(["python3 {} {} {}".format(adjust_size_script,gubbins_phylip_file,partition_file)], shell=True)
		p5.wait()
		abs_output = os.path.abspath(OUTPUT_DIR)
		print("raxml")
		p6 = Popen(["raxmlHPC-PTHREADS -s {} -w {} -n {}_out --asc-cor=stamatakis -q {} -m GTRGAMMAX -T {} -N autoMRE -p 6420662893125220392 -f a -x 7125452922221827660".format(gubbins_phylip_file,abs_output,project_name,partition_file,args["threads"])], shell=True)
		p6.wait()
	else:
		mash_matrix = make_mash_matrix(threads,final_genomes["all_genomes"],OUTPUT_DIR,project_name,temp_dir)
		# with open("test_out.txt","w") as f:
			# f.write(mash_matrix)
		i=2
		matrix = []
		names = []
		firstLine = True
		mash_matrix_lines = mash_matrix.split("\n")
		for line in mash_matrix_lines:
			if line.strip() != "":
				if firstLine:
					print(line)
					current_names = line.split("\t")
					for obj in current_names:
						 if len(obj) > 0:
							 names.append(obj)
					firstLine = False
				else:
					sub_matrix = []
					values = line.split("\t")
					for q in range(1,i):
						val = float(values[q])
						sub_matrix.append(val)
					matrix.append(sub_matrix)
					i+=1
		#print(names)
		#print(len(names),len(matrix))
		print("building tree")
		dm = _DistanceMatrix(names,matrix)
		constructor = DistanceTreeConstructor(method="nj")
		tree = constructor.nj(dm)
		Phylo.write([tree],"my_tree.tree","newick")
	
	
if __name__ == "__main__":
	main()

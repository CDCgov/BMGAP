#!/usr/bin/env python3
### Import Modules ###
import sys
from Bio import SeqIO
import os
import re
import operator
import csv
import pprint as pp
import locale
import argparse
import urllib3
import json
from subprocess import *
#call[("module", "load", "Python/3.4")]
#call[("module", "load", "ncbi-blast+/2.2.29")]
#call[("export", "BLASTDB=/blast/db")]
encoding = locale.getdefaultlocale()[1]
SCRIPT_PATH = os.path.realpath(__file__)
DIR_PATH = os.path.dirname(SCRIPT_PATH)
CUSTOM_DB = os.path.join(DIR_PATH,"custom_allele_sets")
OUTPUT_DIR = ""
skip = ["HAEM1147","HAEM1148","HAEM1149","HAEM1150","HAEM1151","HAEM1152","HAEM1153","HAEM1154","HAEM1155","HAEM1156","HAEM1157","HAEM1158","HAEM1159","HAEM1160","HAEM1161","HAEM1162","HAEM1163","HAEM1164"]
shared_across_species = ["NEIS2210"]
def set_output(output):
	global OUTPUT_DIR
	OUTPUT_DIR = os.path.join(DIR_PATH,output)
	if os.path.isdir(output):
		print("Output Directory",output,"aleady exists, not creating")
	else:
		os.system("mkdir {}".format(output))
		os.system("cp -r {}/hinfluenzae {}".format(CUSTOM_DB,output))
		os.system("cp -r {}/neisseria {}".format(CUSTOM_DB,output))
		print("Created Output Directory",output)

def make_blast_db(allele_fasta,allele_name,mol_type,allele_db_path):
	call(["makeblastdb","-in", allele_fasta,"-input_type","fasta","-title",allele_name,"-dbtype",mol_type,"-out",os.path.join(allele_db_path,allele_name)],shell=False)
	
def main():		
	parser = argparse.ArgumentParser(description="Script for creating local BlastDBs from PubMLST alleles")
	parser.add_argument('-o','--out',help="Create blast DBs here", required=True)
	parser.add_argument('-t','--threads',help="How many threads to use (default=1)", default="1")
	args = vars(parser.parse_args())
	### Print Args ###
	print ("Running with the following parameters:")
	for arg in args:
		print (arg,":",args[arg])
	set_output(args["out"])	
	http = urllib3.PoolManager()
	dna = ["A","G","C","T"]
	db_names = ["neisseria","hinfluenzae"] #PubMLST Species DB names
	for db in db_names:
		loci = "http://rest.pubmlst.org/db/pubmlst_{}_isolates/loci?return_all=1".format(db)
		request = http.request('GET',loci)
		request_data = json.loads(request.data.decode('utf-8'))
		all_loci_dna = ""
		all_loci_prot = ""
		for locus in request_data["loci"]:
			locus_url = locus.replace("isolates","seqdef")
			allele_name = locus_url.split("/")[-1]
			if allele_name in skip:
				continue
			allele_name = allele_name.replace("'","#")
			fasta_request = http.request('GET',locus_url+"/alleles_fasta")
			fasta_data = fasta_request.data.decode('utf-8')		
			if "{" in fasta_data:
				continue # no results found
			allele_db_path = os.path.join(OUTPUT_DIR,"{}".format(db),allele_name.replace("'","#"))
			if os.path.exists(allele_db_path):
				new_allele_count = int(fasta_data.count(">"))
				with open(os.path.join(allele_db_path,"{}.fasta".format(allele_name)),"r") as f:
					existing_file = f.read()
				existing_file_count = int(existing_file.count(">"))
				if new_allele_count == existing_file_count:
					print("no changes detected for {}, skipping".format(allele_name))
					continue
				else:
					os.system("rm -r {}".format(allele_db_path)) #overwrite system
					os.system("mkdir {}".format(allele_db_path))
			else:
				os.system("mkdir {}".format(allele_db_path))
			allele_fasta = os.path.join(allele_db_path,"{}.fasta".format(allele_name))		
			first = True
			with open(allele_fasta,"w") as f:
				f.write(fasta_data)
			first_rec = True
			for seq_record in SeqIO.parse(allele_fasta,"fasta"):
				if first_rec:
					mol_type = "nucl"
					seq = seq_record.seq
					first_rec = False
					for letter in seq:
						if letter not in dna:
							mol_type = "prot"
				else:
					break	
			call(["makeblastdb","-in", allele_fasta,"-input_type","fasta","-title",allele_name,"-dbtype",mol_type,"-out",os.path.join(allele_db_path,allele_name)],shell=False)					
			if allele_name in shared_across_species:
				allele_db_path_hi = allele_db_path.replace("neisseria","hinfluenzae")
				os.system("cp -r {} {}".format(allele_db_path,allele_db_path_hi))
	
		
if __name__ == "__main__":
	main()
				

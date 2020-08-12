#!/usr/bin/env python3.4
### Update mash sketch
### Import Modules ###

import sys
import argparse
import locale
import os
import pprint as pp
from Bio import SeqIO
from subprocess import *
from time import sleep
encoding = locale.getdefaultlocale()[1]



def paste_sketch(threads,mash_db,input_file_path):
	output_db = os.path.basename(mash_db.split(".")[0])
	input_sketch_name = os.path.basename(input_file_path.split(".")[0])
	kmer_size = 32
	sketch_size = 10000
	call(["mash sketch -k {} -p {} -s {} -o {} {}".format(kmer_size,threads,sketch_size,input_sketch_name,input_file_path)], shell=True)
	unique_id = input_sketch_name + output_db
	call(["mash paste {} {} {}.msh".format(unique_id,mash_db,input_sketch_name)],shell=True)
	call(["mv {}.msh {}".format(unique_id,mash_db)],shell=True)
	call(["rm {}.msh".format(input_sketch_name)],shell=True)
	return("added {} to mash db".format(input_file_path))

def main():
	parser = argparse.ArgumentParser(description="Update Mash Sketch")
	parser.add_argument('-f','--file',help="Input file to add to mash sketch", required=True)
	parser.add_argument('-m','--mash_sketch',help="Existing mash sketch", required=True)
	parser.add_argument('-t','--threads',help="Number of max threads to use (default=1)",default="1")
	args = vars(parser.parse_args())
	run = False
	while not run:
		with open("loading_handler.txt","r+") as f:
			lh_text = f.read()
			if "FALSE" in lh_text:
				f.seek(0) 
				f.write("TRUE")
				f.truncate()
				run= True
			if "TRUE" in lh_text:
				sleep(5)
			
	mash_db = args["mash_sketch"]
	threads = args["threads"]
	input_file_path = args["file"]
	input_file = str(os.path.basename(input_file_path))
	#print(input_file)
	## get dict of existing assemblies in mash sketch
	mash_info = check_output(["mash info {}".format(mash_db)],shell=True)
	mash_info = mash_info.decode(encoding)
	mash_info_lines = mash_info.split("\n")
	mash_sketch_assemblies = {}
	for line in mash_info_lines:
		if line.strip() == "":
			continue
		else:
			if "[Hashes]" in line:
				continue
			line = line.replace(" ","***")
			line_items_pre = line.split("***")
			line_items = []
			for obj in line_items_pre:
				if obj.strip() != "":
					line_items.append(obj)
			if len(line_items) == 4:
				assembly_file = line_items[2].split("/")[-1]
				assembly_file = str(os.path.basename(line_items[2]))
				mash_sketch_assemblies[assembly_file] = ""
	if not input_file in mash_sketch_assemblies:
		finished_statement = paste_sketch(threads,mash_db,input_file_path)
		print(finished_statement)
	with open("loading_handler.txt","r+") as f:
		f.seek(0)
		f.write("FALSE")
		f.truncate()


if __name__ == "__main__":
	main()

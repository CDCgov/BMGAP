#!/usr/bin/env python3.4
### Get closest hits
### Import Modules ###

import sys
import argparse
import locale
import os
import re
import json
from collections import OrderedDict
from operator import itemgetter
import pprint as pp
from Bio import SeqIO
from subprocess import *
from time import sleep
encoding = locale.getdefaultlocale()[1]




def pick_genomes(input_file,mash_db,threads,max_num):
	final_result = OrderedDict()
	mash_results = check_output(["mash","dist","-p",threads,mash_db,input_file],shell=False)
	mash_result = re.split(b"\n",mash_results.rstrip())
	#mash_result = mash_results.split("\n")
	lines = [line.decode(encoding).split("\t") for line in mash_result]
	i=0
	for line in sorted(lines,key=itemgetter(2)):
		if i < max_num:
			hit = line[0]
			distance = line[2]
			final_result[hit] = distance
			i+=1
		else:
			break
	return json.dumps(final_result)

def main():
	parser = argparse.ArgumentParser(description="Get closest hits")
	parser.add_argument('-f','--file',help="Input file selection", required=True)
	parser.add_argument('-m','--mash_sketch',help="Existing mash sketch", required=True)
	parser.add_argument('-t','--threads',help="Number of max threads to use (default=1)",default="1")
	parser.add_argument('-n','--max_num',help="Maximum number of results (default=100)",default="100")
	args = vars(parser.parse_args())
	
	input_file = args["file"]
	mash_db = args["mash_sketch"]
	threads = args["threads"]
	max_num = int(args["max_num"])+1
	
	final_result = pick_genomes(input_file,mash_db,threads,max_num)
	pp.pprint(final_result)
	
	


if __name__ == "__main__":
	main()

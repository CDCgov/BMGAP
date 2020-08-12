#!/usr/bin/env python3
### Phylogeny Building Tool v1
### Import Modules ###
import sys
from Bio import SeqIO
from Bio.Phylo.TreeConstruction import DistanceCalculator
from Bio.Phylo.TreeConstruction import _DistanceMatrix
from Bio.Phylo.TreeConstruction import DistanceTreeConstructor
from Bio import Phylo
import os
import locale
import argparse
import datetime
import re
import operator
import json
import time
import shutil
import math
import tempfile
from operator import attrgetter
from subprocess import *
encoding = locale.getdefaultlocale()[1]

def make_mash_matrix(input_data,temp_dir,threads):
    print("Running Mash")
    kmer_size = 32
    sketch_size = 10000
    with open(os.path.join(temp_dir,"temp_assembly_list"),"w") as f:
        for obj in input_data:
            f.write("{}\n".format(obj))
    mash_assembly_list = os.path.join(temp_dir,"temp_assembly_list")
    unique_time = str(time.time()).split(".")[1]
    out_sketch_name = "fast_phylo_{}".format(unique_time)
    output_sketch = os.path.join(temp_dir,out_sketch_name)
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



def main():
    ### Main Arg Parse ###
    parser = argparse.ArgumentParser(description="Fast tree builder v1")
    parser.add_argument('-i','--input',help="Input list of assembly paths")
    parser.add_argument('-t','--threads',help="Threads for mash)",default="1")
    args = vars(parser.parse_args())
    start_time = time.time()
    temp_dir = tempfile.mkdtemp()
    genome_list = args["input"] # List of assembly paths
    with open(genome_list) as f:
        input_data = f.read().strip().split("\n")
    threads = args["threads"]
    mash_matrix = make_mash_matrix(input_data,temp_dir,threads)
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
    #print(names,len(names))
    #print(len(names),len(matrix))
    print("building tree")
    dm = _DistanceMatrix(names,matrix)
    constructor = DistanceTreeConstructor(method="nj")
    tree = constructor.nj(dm)
    unique_time = str(time.time()).split(".")[1]
    Phylo.write([tree],"my_tree_{}.tree".format(unique_time),"newick")

if __name__ == "__main__":
    main()

import os
import sqlite3
import sys
import re

input_file = sys.argv[1]
conn = sqlite3.connect("../sqlite3_db/species_db_v1")
c = conn.cursor()

def add_organism(genus,species):
	print("select * from Organism where genus='{}' and species='{}'".format(genus,species))
	c.execute("select * from Organism where genus='{}' and species='{}'".format(genus,species))
	org_res = c.fetchone()
	if org_res:
		print("Found existing entry for {} with {}".format(genus,species))
		my_entry = org_res[0]
	else:
		print("insert into Organism ('genus', 'species') values ('{}','{}')".format(genus,species))
		c.execute("insert into Organism ('genus', 'species') values ('{}','{}')".format(genus,species))
		conn.commit()
		my_entry = c.lastrowid
	return my_entry

def add_source(source):
	print("select * from Source where source_location='{}'".format(source))
	c.execute("select * from Source where source_location='{}'".format(source))
	org_res = c.fetchone()
	if org_res:
		print("Found existing entry for {}".format(source))
		my_entry = org_res[0]
	else:
		print("insert into Source ('source_location') values ('{}')".format(source))
		c.execute("insert into Source ('source_location') values ('{}')".format(source))
		conn.commit()
		my_entry = c.lastrowid
	return my_entry
	
def add_genome(lab_id,organism_id,file_name,source_id):
	print("select * from Genome where lab_id='{}' and organism_id='{}' and filepath='{}' and source_id='{}'".format(lab_id,organism_id,file_name,source_id))
	c.execute("select * from Genome where lab_id='{}' and organism_id='{}' and filepath='{}' and source_id='{}'".format(lab_id,organism_id,file_name,source_id))
	org_res = c.fetchone()
	if org_res:
		print("Found existing entry for lab_id {} ".format(lab_id))
		my_entry = org_res[0]
	else:
		print("insert into Genome ('lab_id','organism_id','filepath','source_id') values ('{}','{}','{}','{}')".format(lab_id,organism_id,file_name,source_id))
		c.execute("insert into Genome ('lab_id','organism_id','filepath','source_id') values ('{}','{}','{}','{}')".format(lab_id,organism_id,file_name,source_id))
		conn.commit()
		my_entry = c.lastrowid
		
def main():
	with open(input_file) as f:
		for line in f:
			if line.strip() != "":
				line = line.rstrip()
				print(line)
				lab_id = line.split('\t')[0]
				genus = line.split('\t')[1]
				species = line.split('\t')[2]
				source = line.split('\t')[3]
				file_name = line.split('\t')[4]
				organism_id = add_organism(genus,species)
				print(organism_id)
				source_id = add_source(source)
				print(source_id)
				add_genome(lab_id,organism_id,file_name,source_id)
			
		
if __name__ == "__main__":
	main()
	

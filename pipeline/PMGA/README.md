# PMGA - PubMLST Genome Annotator v2.0


Current Species Included:

 * All Neisseria species
 * *Haemophilus influenzae*

**Dependencies**
```
module load Python/3.7
module load ncbi-blast+/LATEST
module load Mash/1.1 (if no BMScan Json provided)
```
How to use:
1) Generate local PubMLST Allele Blast Databases using build_pubmlst_dbs.py script


**Recommended usage to include prebuilt custom DBs** 

```python
python3.7 build_pubmlst_dbs.py -o pubmlst_dbs_all
```

* This usage will copy all prebuilt allele folders from the custom_allele_set directory into the pubmlst_dbs_all folder.
* If given a previously-existing PubMLST Allele Database, the script will check for changes within each allele.
* If changes are identified, the allele collection will be updated, if not, it will move on to the next allele set. 


2) Annotate Genomes using blast_pubmlst.py script
```python
usage: blast_pubmlst.py [-h] -d INDIR [-b BLASTDIR] [-c CHAR] [-sg] [-pr]
                           [-fa] [-fr] -o OUT [-j JDEBUG] [-jf FDEBUG]
                           [-s SPECIES] [-t THREADS]
Version 2.0 - Script for annotating genomes using PubMLST allele set
optional arguments:
  -h, --help            show this help message and exit
  -d INDIR, --indir INDIR
                        Input Dir
  -b BLASTDIR, --blastdir BLASTDIR
                        Directory containing blast DBs
                        *Will default to "pubmlst_dbs_all"
  -c CHAR, --char CHAR  Characterizations File
  -sg, --serogroup      Produce SG prediction file
  -pr, --promoters      Identify Promoters (*Experimental*)
  -fa, --fastas         Output identified gene sequences as FASTAs
  -fr, --force          Force overwrite existing output file
  -o OUT, --out OUT     Output Directory
  -j JDEBUG, --jdebug JDEBUG
                        Skip step 1 by providing existing JSON folder with raw blast results
  -jf FDEBUG, --fdebug FDEBUG
                        Skip step 2 by providing existing JSON folder with final results
  -s SPECIES, --species SPECIES
                        BMScan Json input to skip running BMScan again
  -t THREADS, --threads THREADS
                        Number of Threads to use (default=1)
```

### Output Files
* The output directory will consist of the following:

1) **JSON** - contains 2 JSON files per assembly: "raw" contains the unfiltered BLAST results, and "final" contains the filtered, final blast results

2) **GFF** - contains 1 GFF file per assembly: contains same information as found in the final JSON in GFF format

3) **Serogroup** - contains serogroup predictions if "-sg" flag was provided

4) **Feature_fastas** - contains fasta files per feature if "-fa" flag was provided

5) **Summary** - contains group comparison summary files if "-c" flag was provided


### PMGA Modules

#### 1) Serogroup Prediction
* This module can be accessed through the "-sg" flag.
* It currently only works on *Neisseria* species, and is designed for *Neisseria meningitidis*
* Identifies serogroup backbone of sample, and attempts to predict expression of capsule based on identified mutations, presence of essential genes, disruption of genes by insertion elements, and more

#### 2) Group Comparison
* This module can be accessed through the "-c" flag
* The input is a tab-delimited file containing the name of the file and the group, for example:
```
my_file_1.fasta	group_1
my_file_2.fasta	group_1
my_file_3.fasta	group_1
my_file_4.fasta	group_2
my_file_5.fasta	group_2
my_file_6.fasta	group_2
```
* Output will consist of:
1) Frequency of presence of each gene per group
2) Frequency of each allele identified per group
3) Frequency of each non-functional (ie. internal stop) allele identified per group
* These will be found in the "summary" folder

#### 3) Fasta Output

* This module can be accessed through the "-fa" flag
* It will generate fasta files per assembly  containing all features identified, such as CDS (coding regions), IGR (intergenic regions and non-coding regions), PRO (promoters) and more

### Additional Information

* db contains SQlite3 DB with functional annotation information for each gene.
* These were obtained via InterProScan
* These currently exist only for Neisseria alleles - currently working on annotating *Haemophilus influenzae* alleles

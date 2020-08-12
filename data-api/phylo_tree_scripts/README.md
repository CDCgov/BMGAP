# Fast phylogenetic tree builder (BMGAP version)

## Dependencies:

```
Python/3+ (with BioPython)
Mash/2.0
```

```
usage: build_phylo_fast_bmgap.py [-h] [-i INPUT] [-t THREADS]

Fast tree builder v1

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input list of assembly paths
  -t THREADS, --threads THREADS
                        Threads for mash)
```

Takes a list file of assembly paths and uses Mash and BioPython to generate a neighbor joining tree. Output file is in newick format. 

# Automated Phylogenetic Tree Builder

## Dependencies:

```
Python/3.4
Mash/2.0
snippy/3.1
gubbins
raxml/8.2.9
```

## Usage
```
usage: build_phylo.py [-h] [-d INDIR] -o OUT [-t THREADS] [-b MASH_DB] [-f]
                      [-m MAX_NUM] [-fr] [-g GENOMES] [-r REFERENCE]
                      [-s SNIPPY] -p PROJ_NAME

Automated Phylogeny Builder v1

optional arguments:
  -h, --help            show this help message and exit
  -d INDIR, --indir INDIR
                        Input Directory: Directory of FASTA files to analyze
  -o OUT, --out OUT     Output Directory
  -t THREADS, --threads THREADS
                        Number of max threads to use (default=1)
  -b MASH_DB, --mash_db MASH_DB
                        Provide prebuilt mash DB, otherwise build from scratch
  -f, --fast            Fast option for distance based neighbor joining tree
  -m MAX_NUM, --max_num MAX_NUM
                        Maximum number of isolates to include (default=50)
  -g GENOMES, --genomes GENOMES
                        Provide genome directory to build tree with instead of
                        automatically picking, requires -r flag
  -r REFERENCE, --reference REFERENCE
                        Required with -g flag; provide reference to use for
                        phylogeny when providing genome directory
  -s SNIPPY, --snippy SNIPPY
                        existing snippy dir, requires -g and -r
  -p PROJ_NAME, --proj_name PROJ_NAME
                        project prefix - will be used to label all files
                        associated with project
```

## Examples:

``` build_phylo.py -d my_fastas -t 3 -m 100 -p first_run -o first_run_out ```

The first time this program runs, it will first create a mash DB from BMGAP that have passed QC.
Use the -b flag to refer to this mash DB for future uses of the script

Example:

``` build_phylo.py -d my_fastas -t 3 -m 100 -p first_run -o first_run_out -b my_mash_db.msh```

This script can also be run on an existing genome directory (-g)  with a reference specified (-r)

Example:

``` build_phylo.py -g my_fastas -t 5 -r reference/fam18.fasta -p cc11_phylo -o cc11_phylo_out```


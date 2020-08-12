(help message from v1.5.7)
usage: LocusExtractor.py [-h] [--version] [-p PROJECTID] [-s SETTING_DIR]
                         [-m MIN_COV] [--debug] [--no_update]
                         [--shallow_search_assemblies] [--export_best_match]
                         [--preserve_BLAST_hits]
                         ...

A program to identify and report specific sequences in genomes.

positional arguments:
  args

optional arguments:
  -h, --help            show this help message and exit
  --version, -V         show program's version number and exit
  -p PROJECTID, --projectID PROJECTID
                        Provide an identifier that will be added to output
                        directory and data table
  -s SETTING_DIR, --setting_dir SETTING_DIR
                        Location of setting files
  -m MIN_COV, --min_cov MIN_COV
                        Alternate minimum coverage
  --debug               Do not update reference files. Same as 'no_update'
  --no_update           Do not update reference files. Same as 'debug'
  --shallow_search_assemblies
                        Do not search subdirectories for assemblies
  --export_best_match   Export files comparing new alleles to their best
                        match.
  --preserve_BLAST_hits
                        Keep raw BLAST result files

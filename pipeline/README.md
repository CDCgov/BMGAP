#BMGAP Pipeline

This repository contains the code that makes up the the analysis portion of the BMGAP pipeline. It includes the code to run the pipeline and to ingest results from the filesystem.

##Prerequistes

The pipeline runs using Bash v4.0+ and Python 3.6+. The pipeline expects the required python packages to be installed in a virtual environment named bmgap placed in the directory where the pipeline scripts are kept. There is a requirements.txt file included with the pipeline to automate the process of installing the required libraries after the creation of the virtual environment

```code
virtualenv bmgap
source bmgap/bin/activate
pip install -r requirements.txt
```

The BMGAP pipeline uses lmod to manage dependencies. If you don't have access to lmod, this pipeline can be updated by commenting out lines with the command "ml" or "module load" and ensuring that MASH 2.0 and the NCBI BLAST suite (blastn and makeblastdb at minimum) are on the path.

##Pipeline

The pipeline is run by the script BML-External-Runner.sh. This script is run from the sample directory and takes two arguments - a path where the scripts are loated and a URL for the monogoDB host.

##Ingesting Data

The pipeline automatically ingests data when analysis process runs. Data is stored in a mongoDB database, described in detail in the ../database/ directory. The script BML-Data-Reingestion.sh is run from the sample directory providing script path and mongoDB host as arguments. The script ensures the identifier on the filesystem points to the correct sample in the database, and does not overwrite existing entries unless directed.


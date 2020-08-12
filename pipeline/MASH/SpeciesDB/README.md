# BMScan- A rapid and accurate tool to delineate bacterial meninigitis causing species. 

### Target Species

```
#### Bacterial meningitis causing organisms
N. meningitidis
H. influenzae
S.pneumoniae
L.monocytogenes
E.coli

#### Other Neisseria sp. of interest
N. polysaccharea
N. bergeri
N. weaveri
N. subflava
N. mucosa
N. lactamica
N. gonorrhoeae
N. elongata
N. cinerea

#### Other Haemophilus sp. of interest
H. parainfluenzae
H. parahaemolyticus
H. haemolyticus

```

### Usage
```
usage: identify_species.py [-h] [-d INDIR] [-v] [-j] [-t THREADS] [-o OUT]

Script for quickly determining species

optional arguments:
  -h, --help            show this help message and exit
  -d INDIR, --indir INDIR
                        Input Directory: Directory of FASTA files to analyze
  -v, --verbose         verbose standard output (default = false)
  -o OUT, --out OUT     Output File name
  -j, --json 			Output only JSON file (default = false)
  -t THREADS, --threads THREADS
                        Number of max threads to use (default=1)
```

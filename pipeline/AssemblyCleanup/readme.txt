The main script in this package is cleanupSingle.py.

It takes a SPADES assembly, calculates some QC statistics, and separates high-quality contigs from those that are likely spurious (based on length and coverage), then recalculated the QC stats
Below is an example of a Aspen script that would run it, along with usage notes...

#!/bin/bash -l
#$ -cwd


module load Python/3.4 ##Make sure this has pandas, matplotlib is good.

python3 ./cleanupSingle.py -p 0.1 -b TestGenome $1 $2
##-b needs to be replaced with the "Base_ID" for each genome.


##Usage: options, input file (.fasta) and output file (.fasta)
## The directory for the output file must already exist. The parameter Base_ID (-b) must be specified for each genome. The parameter -p should be left at the indicated value of 0.1 
# This will create three text files for each genome: The given output file, a "discard" file with the term '_discarded' appended to the output filename. And a "report" table (tab-delimited).
## If Matplotlib is available in Python, it will also make a scatter plot of contig size vs covereage (PNG)
  
##  The statistics for the original file have the suffix "_raw", while the stats for the final file have no suffix (e.g. Contig_Count_raw vs Contig_Count)
## The default filter is rather liberal -- contigs > 250bp and coverage >5x (the -p value adds the requirement that they also have > 10% of mean depth of coverage). When we have good data (250bp reads, paired end; ~100x coverage). 

#

## Dependencies:

```
Python/3.4
Mash/2.0
```


## Usage Instructions:


### First Script: **build_bmgap_mash_sketch.py**
##### Run once to build a mash sketch from all assemblies in BMGAP
##### NOTE - Only assemblies that have passed QC are included in the mash sketch

```
usage: build_bmgap_mash_sketch.py [-h] -o OUT [-t THREADS]

Build BMGAP mash sketch

optional arguments:
  -h, --help            show this help message and exit
  -o OUT, --out OUT     Location of output
  -t THREADS, --threads THREADS
                        Number of threads to use (default=1)
						
```

### Second Script: **update_mash_sketch.py**
##### Takes a single assembly as input to be added to the existing mash sketch collection
##### This script was designed to be run in parallel, so to avoid IO errors, an included loading_handler.txt file manages which process currently has access to the mash sketch

```
usage: update_mash_sketch.py [-h] -f FILE -m MASH_SKETCH [-t THREADS]

Update Mash Sketch

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Input file to add to mash sketch
  -m MASH_SKETCH, --mash_sketch MASH_SKETCH
                        Existing mash sketch
  -t THREADS, --threads THREADS
                        Number of max threads to use (default=1)
```

### Third Script: **get_closest_hits.py**
##### Returns an ordered dictionary object containing the top X + 1 closest hits to the query assembly
##### Note - Since the first top hit is the query isolate, so script returns 1 additional hit

```
usage: get_closest_hits.py [-h] -f FILE -m MASH_SKETCH [-t THREADS]
                           [-n MAX_NUM]

Get closest hits

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Input file selection
  -m MASH_SKETCH, --mash_sketch MASH_SKETCH
                        Existing mash sketch
  -t THREADS, --threads THREADS
                        Number of max threads to use (default=1)
  -n MAX_NUM, --max_num MAX_NUM
                        Maximum number of results (default=100)
```

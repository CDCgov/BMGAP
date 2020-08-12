#  AmpliconExtractor.py
#  
# Created by Adam Retchless for the Meningitis lab in the CDC, under contract with IHRC. Inc.
#  Adam Retchless <aretchless@cdc.gov>
#  
#
#
#
#pylint: disable=bad-indentation,global-statement, broad-except

import os
import pandas as pd
import re
import sys
import genomeOrganizer
import utilities
import tempfile
# from subprocess import call, DEVNULL
from Bio.Blast.Applications import NcbiblastnCommandline
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC
from BLASThelpers import makeblastdb, loadBLASTtableToDataFrame,blankBLASTtable
from shutil import copytree


# _primer_file = 'settings/sample-primers.csv'
default_verbose = __name__ == "__main__"
current_verbose = default_verbose 

script_version=1
script_subversion = 5

def vprint(text):
    if current_verbose:
        print(text)    

def print(text):#pylint: disable=redefined-builtin
    export_text = "{}".format(text)
    if __name__ != "__main__":
        export_text = "\t"+export_text
    sys.stdout.write(export_text+"\n")
        
def read_file_to_dict(filename):
    primer_cols = ['Locus','Role','Region','Name','Direction','Sequence']
    primer_frame = pd.read_table(filename,comment='#',dtype=str,skip_blank_lines=True) #skip blank lines is true by default
    ###Skip blank lines does not work
    primer_frame = primer_frame.dropna(how='all')
    primer_frame['Direction'].fillna('',inplace=True)
    primer_frame['Region'].fillna('All',inplace=True)
    primer_dict = dict()
    for _, row in primer_frame.iterrows():
        ##Parse
        locus = row['Locus']
        region = row['Region']
        primer = row['Name']
        sequence = row['Sequence']
        direction = row['Direction']
        ##Role can be a list
        function = []
        role = row['Role']
        if re.match('PCR',role,re.IGNORECASE):
            function = ['PCR'] 
        elif re.match('Seq',role,re.IGNORECASE):
            function = ['Seq']
        elif re.match('All',role,re.IGNORECASE):
            function = ['PCR','Seq']
        else: ##Did not find function, use for both steps
            function = ['PCR','Seq']
            vprint("Did not identify function of primer {} -- use for both PCR and Seq".format("-".join([locus,primer])))
            vprint('To assign a function, write "PCR", "Seq", or "All" in the second column')
        ##Construct dict of dict     
        if locus not in primer_dict:
            primer_dict[locus] = dict()
        locus_dict = primer_dict[locus]
        for f in function: #Add data to both PCR and Seq if appropriate
            if f not in locus_dict:
                locus_dict[f] = dict()
            function_dict = locus_dict[f]
            if region not in function_dict:
                function_dict[region] = dict()
            region_dict = function_dict[region]
            region_dict[primer] = sequence
            ##TODO add direction
#     
# 
#     _primer_dict = dict() ## Dict of Dicts: locus, function (PCR,Seq),region,name,sequence
#     with open(filename) as primers:
#             p_reader = csv.reader(primers)
#             p_reader = [row for row in p_reader if not row[0].startswith('#')] #strip comments
#             for row in p_reader:
#                     row = [item for item in row if item != ''] #strip empy strings
#                     if len(row) > 0:
#                             vprint("Parsing row with {} items".format(len(row)))
#                             ##First is locus name -- no exception
#                             locus = row[0]
#                             ##Last is sequence -- no exception
#                             sequence = row[-1].replace(" ","")
#                             ##Second to last is primer name -- no exception
#                             primer = row[-2]
#                             vprint("Name is {}-{}".format(locus,primer))
#                             ##Function and region are optional
#                             c_max = len(row) - 3 #last two indexes are used, so -3 is the maximum that is  open
#                             c = 1
#                             ##Second could be function (PCR,Seq,All)
#                             if c <= c_max:
#                                     function = []
#                                     if re.match('PCR',row[c],re.IGNORECASE):
#                                             function = ['PCR'] 
#                                             c+=1
#                                     elif re.match('Seq',row[c],re.IGNORECASE):
#                                             function = ['Seq']
#                                             c+=1
#                                     elif re.match('All',row[c],re.IGNORECASE):
#                                             function = ['PCR','Seq']
#                                             c+=1
#                                     else: ##Did not find function, use for both steps
#                                             function = ['PCR','Seq']
#                                             vprint("Did not identify function of primer {} -- use for both PCR and Seq".format("-".join([locus,primer])))
#                                             vprint('To assign a function, write "PCR", "Seq", or "All" in the second column')
#                             region = 'All'
#                             if c <= c_max:
#                                     region = row[c]
#                             if locus not in _primer_dict:
#                                     _primer_dict[locus] = dict()
#                             locus_dict = _primer_dict[locus]
#                             for f in function: #Add data to both PCR and Seq if appropriate
#                                     if f not in locus_dict:
#                                             locus_dict[f] = dict()
#                                     function_dict = locus_dict[f]
#                                     if region not in function_dict:
#                                             function_dict[region] = dict()
#                                     region_dict = function_dict[region]
#                                     region_dict[primer] = sequence
#     #~ print("Found primers for the following genes: "+";".join(_primer_dict.keys())) #Not accurate. Does not confirm that dict contains primers
    return primer_dict
                
## map_primers_to_genome will use BLAST to identify where primers are likely to bind in the genome.
# _primer_dict is a primer heirarchy as returned by "read_file_to_dict"
# blast_db is the name of the genome db you want to search
# outfile is destination to write the blast results to. If outfile is given, we assume that you want details about where the primers map and will put minor warnings to stdout; otherwise, we assume you don't care and the are suppressed
# ## User can "cheat" by passing "range_from" and "range_to" integers in the locus dict. 
# Returns : export_regions[locus][subregion][name] = {'contig','start','stop'} where start and stop are the first coordinates past the low and high primers

## Returns a dict with genome information (key in CAPS): isolate NAME, ORIGINAL filename, FASTA filename, blast DB name, contig SEQS
def setupGenomeForBlastBasedExtraction(genome_name,genome_file,tempDir,file_format = '',is_compressed = None):
    ##Genome information 
    genomeInfo = dict()
    genomeInfo['name'] = genome_name
    genomeInfo['original'] = genome_file #just for reporting
    ##Some people use weird genome filenames, so I need to copy it to something without special characters
    temp_genome = os.path.join(tempDir,genome_name + '.fasta')
    genomeOrganizer.exportGenomeFASTA(genome_file,temp_genome,file_format,is_compressed)
    genomeInfo['fasta'] = temp_genome   
    if not os.path.isfile(genomeInfo['fasta']):
        raise IOError("Illegitimate file at "+genomeInfo['fasta'])
    #~ genomeDir,genomeFile = os.path.split(os.path.abspath(genomeInfo['fasta']))
    #open the genome file for extracting sequences
    genome_handle = utilities.flexible_handle(genomeInfo['original'], is_compressed, 'rt')
    genomeInfo['seqs'] = SeqIO.to_dict(SeqIO.parse(genome_handle, file_format))
    print("{} bp in {} contig(s)".format(sum([len(c) for c in genomeInfo['seqs'].values()]),len(genomeInfo['seqs']))) ##Appends to sequence identifier line
    if len(genomeInfo['seqs']) == 0:
        raise ValueError("No sequences parsed from file {}".format(genomeInfo['fasta']))
    genome_handle.close()      
    # make search database for genome
    db_base = os.path.basename(genomeInfo['fasta'])
    genomeInfo['db'] = os.path.join(tempDir,db_base)
    makeblastdb(genomeInfo['fasta'],genomeInfo['db'])  
    return genomeInfo
    
class AmpliconExtractor:
    def __init__(self,primer_file,working_dir=None,generate_output=False):
        ###  Make writable directories
        if working_dir is None:
            working_dir = os.getcwd() 
        ##utilities.safeMakeOutputFolder(os.path.join(working_dir,'AmpExtTemp'))
        self.generate_output = generate_output   
        self.primers_dict = read_file_to_dict(primer_file)            
        if generate_output:
            self.outDir = utilities.safeMakeOutputFolder(os.path.join(working_dir,'AmpliconExtractor'))
            self.sequence_files = {locus: os.path.join(self.outDir,'{}_primer-extracted_sequences.fasta'.format(locus)) for locus in self.primers_dict.keys()}
            self.amplicon_info_file = os.path.join(self.outDir,'amplicon_information.tab')
            self.tempDirObj = tempfile.TemporaryDirectory(suffix='_AmpExt', prefix='tmp', dir=self.outDir)
        else:
            self.outDir = self.sequence_files = self.amplicon_info_file = None
            self.tempDirObj = tempfile.TemporaryDirectory(suffix='_AmpExt', prefix='tmp', dir=working_dir)
        
        self.amplicon_info_list = []


        
    ##Full service function for a single genome
    def evaluateGenome(self,genome_name,genome_file,file_format = '',is_compressed = None, keep_temp = False):
        print("## Begin searching sequence {} ## ".format(genome_name))
        primer_hit_file = None
        if self.outDir is not None:
            primer_hit_file = os.path.join(self.outDir,'primer_hits.tab')
            primer_hit_file = utilities.appendToFilename(primer_hit_file, genome_name)
        genomeInfo = setupGenomeForBlastBasedExtraction(genome_name,genome_file,self.tempDirObj.name,file_format,is_compressed)
        amplicon_info = {'Filename':genome_file,"Lab_ID":genome_name}
        primers_loc  = self.map_primers_to_genome(genomeInfo['db'],primer_hit_file,keep_temp=keep_temp)
        for locus, locus_dict in primers_loc.items():
            for subregion, subregion_dict in locus_dict.items():
                if isinstance(subregion_dict,dict): ##Sequencing features
                    for name,locations in subregion_dict.items():
                        print('Seq name :'+ name)
                        contig = locations['contig']
                        print('On contig: '+contig)
                        contig_seq = genomeInfo['seqs'][contig]
                        print('Found contig: {}, length {}'.format(contig_seq.id,len(contig_seq)))
                        start = locations['start']
                        print('Start: {}'.format(start))
                        stop = locations['stop']
                        print('Stop: {}'.format(stop))
                        my_seq = contig_seq[start:stop+1]
                        new_name = name.replace(' ','_')
                        my_seq.id = new_name
                        my_seq.description ="{}:{}-{}".format(contig,start,stop)
#                         my_fasta = SeqRecord(my_seq,id=name.replace(' ','_'),description="{}:{}-{}".format(contig,start,stop))
                        if self.sequence_files is not None:
                            with open(self.sequence_files[locus],"a") as fout:
                                SeqIO.write(my_seq,fout,'fasta')
                            if file_format == 'fastq':
                                fastq_file = utilities.setExt(self.sequence_files[locus], 'fastq', False)
                                with open(fastq_file,'a') as fastq_out:
                                    SeqIO.write(my_seq,fastq_out,'fastq') 
                elif subregion == 'OuterRange': ##Original amplicon...actually a range
                    range_list = subregion_dict
                    for item in range_list:
                        assert isinstance(item,region_record)
                    if len(range_list) == 1:
                        rr = range_list[0]
                        amplicon_info['{}_PCR_size'.format(locus)] = "{}".format(rr.get_max() - rr.get_min() + 1)
                        amplicon_info['{}_contig'.format(locus)] = "{}".format(rr.contig) 
                        amplicon_info['{}_start_position'.format(locus)] = "{}".format(rr.get_min()) 
                        amplicon_info['{}_stop_position'.format(locus)] = "{}".format(rr.get_max())  
                        
                        #TODO: report something
                else:
                    print("Warning feature {} not reported for locus {}".format(subregion,locus))
        self.amplicon_info_list.append(amplicon_info)
    
    ##Returns a dict with entry for every locus that was searched for
    #Tolerance keeps hits with bit-scores at tolerance*max_score
    def map_primers_to_genome(self,blast_db,outfile=None,search_set=None,default_to_PCR=False,temp_dir = None, keep_temp=False, tolerance=1):
        workingDir = temp_dir if temp_dir is not None else self.tempDirObj.name
        if outfile == '':
            outfile = None
        if search_set == None:
            search_set = set(self.primers_dict.keys())
        temp_infile = os.path.join(workingDir,'tmp_primer.fasta')
        temp_outfile = os.path.join(workingDir,'tmp_primer_blast.fasta')
        blast_combined = blankBLASTtable()
        ql_head = 'query_length' #new column to add
        fh_head = 'forward hit'
        export_regions = dict() #name for region, coordinates of innermost nucleotide on outermost primers (draw data from seq_borders dict in the sequencing reaction)
        for locus in search_set:
            if locus not in self.primers_dict.keys():
                print("Error: {} is not in the set of primer loci".format(locus))
            locus_dict = self.primers_dict[locus].copy() #so that I can modify it
            if default_to_PCR: #Make sure there are primers for sequencing the entire region
                seq_dict = locus_dict['Seq']
                if 'All' not in seq_dict.keys():
                    seq_dict['All'] = locus_dict['PCR']['All']
            export_regions[locus] = dict()
            ##Evaluate PCR dict first to find general range in which sequencing primers can bind
            PCR_dict = locus_dict['PCR']
            range_list = []
            ## Create a master range limit if specified
            has_range = ('range_contig' in locus_dict.keys()
                        and 'range_from' in locus_dict.keys() 
                        and 'range_to' in locus_dict.keys())
            if has_range:
                master_range = region_record(locus_dict['range_contig'],locus_dict['range_from'],locus_dict['range_to'])
                range_list.append(master_range)
            ## Place BLAST hits into ranges
            for (subregion, subregion_dict) in PCR_dict.items(): ##Only one region: "all"
                for (primer,sequence) in subregion_dict.items():
                    #Write query file
                    my_seq = SeqRecord(Seq(sequence,IUPAC.ambiguous_dna),id="-".join([locus,'PCR',subregion,primer]))
                    with open(temp_infile,"w") as fout:
                            SeqIO.write(my_seq,fout,'fasta')
                    #Search BLAST
                    blast_cline = NcbiblastnCommandline(query=temp_infile,db=blast_db,outfmt=6,out=temp_outfile,task='blastn-short',evalue=1,reward=1,penalty=-1,gapopen=3,gapextend=2)
                    blast_cline() ##Should only print for errors
                    blast_table = loadBLASTtableToDataFrame(temp_outfile)
                    if keep_temp:
                        named_file = '{}_{}.tab'.format("-".join([locus,'PCR',subregion,primer]),os.path.basename(blast_db)) 
                        utilities.safeOverwriteTable(os.path.join(workingDir,named_file), blast_table, 'tab')
                    ##SPlace best hits into ranges
                    if len(blast_table) > 0:
                        ##Add some extra info to table
                        blast_table[ql_head] = len(my_seq)
                        blast_table[fh_head] = blast_table['s. start'] < blast_table['s. end']
                        ## Limit table to best hits
                        best = blast_table.sort_values(by=['bit score'],ascending=False).iloc[0]
                        best_table = blast_table[blast_table['bit score'] >= tolerance*best['bit score']] #This may be too stringent; may need to revisit
                        ## Add best hits to ranges
                        for _,this_hit in best_table.iterrows():
                            finished = False #if we found a range for it
                            for this_range in range_list:
                                if not finished: #stop upon success or if range is exclusive
                                    finished = this_range.try_add_primer(this_hit['subject id'],this_hit['s. start'],this_hit[fh_head],True)
                                    if this_range.exclusive and not finished:
                                        finished = True
                                        if len(best_table) == 1:
                                            print("Warning: an exclusive hit failed to map to the prespecified region. Please report to developer(s)")
                            if not finished:
                                new_range = region_record()
                                new_range.try_add_primer(this_hit['subject id'],this_hit['s. start'],this_hit[fh_head],True)
                                range_list.append(new_range)
                        
                        ## Record best hits for reporting
                        blast_combined = pd.concat([blast_combined,best_table],sort=True)##Note: this is compatible with pandas 0.23 +; older versions will fail. Without sort, it makes FutureWarning and exception.
                    else:
                            print("Warning: zero hits for {}".format(my_seq.id))
            ##Merge any ranges that are close/overlapping; test if ranges are valid (primer pairs)
            i = 0
            ValidRanges = set()
            while i < len(range_list):
                this_range = range_list[i]
                j = len(range_list)-1
                while j > i:
                    merger = this_range.try_merge_regions(range_list[j])
                    if merger:
                        print("Warning: this is an exceptional situation and has not been tested, please report to developer(s). Range merger")
                        del(range_list[j])
                    j-=1
                #Test validity of this_range
                if (len(this_range.For_list) > 0 and len(this_range.Rev_list) > 0):
                    if this_range.get_min() < this_range.get_max():
                        ValidRanges.add(i)
                i+=1
            #Remove invaled ranges
            range_list = [range_list[i] for i in ValidRanges]
            #Report oddities
            if len(range_list) == 0:
                print("Warning: Unable to find an amplification region for {}".format(locus))
            elif len(range_list) == 2:
                print("Warning: Detected multiple amplification regions for {}".format(locus))
            for this_range in range_list:
                vprint('\n'+locus + ": Potential amplicon region")
                vprint(this_range)
                    
            ## Find the sequencing sites within the defined ranges
            Seq_dict = locus_dict['Seq']
            for (subregion, subregion_dict) in  Seq_dict.items():
                    export_regions[locus][subregion] = dict()
                    seq_borders = dict() ##Use range as key to track where sequencing of subregion starts. Values outside of range indicate no matches
                    seq_primers = dict() ##primer names corresponding to border positions
                    for (primer,sequence) in subregion_dict.items():
                            my_seq = SeqRecord(Seq(sequence,IUPAC.ambiguous_dna),id="-".join([locus,'Seq',subregion,primer]))
                            with open(temp_infile,"w") as fout:
                                    SeqIO.write(my_seq,fout,'fasta')
                            blast_cline = NcbiblastnCommandline(query=temp_infile,db=blast_db,outfmt=6,out=temp_outfile,task='blastn-short',evalue=1,reward=1,penalty=-1,gapopen=3,gapextend=2)
                            blast_cline() ##Should only print for errors
                            blast_table = loadBLASTtableToDataFrame(temp_outfile)
                            if len(blast_table) > 0:
                                    ##Add some extra info to table
                                    blast_table[ql_head] = len(my_seq)
                                    blast_table[fh_head] = blast_table['s. start'] < blast_table['s. end']
                                    for my_range in range_list:
                                            ## Limit table to hits in range
                                            r_min = my_range.get_min()
                                            r_max = my_range.get_max()
                                            if my_range not in seq_borders: ##TODO: this should probably be initialized immediately after declaration. Need to check that it doesnt' break the downstream features
                                                    seq_borders[my_range] = [r_min -1, r_max+1]
                                                    seq_primers[my_range] = ['None','None']
                                            range_table = blast_table[blast_table['subject id'] == my_range.contig]
                                            range_table = range_table[range_table['s. end'] >= r_min]
                                            range_table = range_table[range_table['s. end'] <= r_max]
                                            if len(range_table) > 0:
                                                    ## Limit table to best hits
                                                    best_in_range = range_table.sort_values(by=['bit score'],ascending=False).iloc[0]
                                                    range_table = range_table[range_table['bit score'] >= best_in_range['bit score']] #This may be too stringent; may need to revisit
                                                    if len(range_table) > 0:
                                                            if len(range_table) > 1:
                                                                    export_line = "Warning: sequencing primer maps to multiple locations within PCR primers. Using outermost site: {}".format(my_seq.id)
#                                                                     if __name__ != "__main__": ##Being called from an outside procedure...indent to indicated subsidiary position
#                                                                         export_line = '\t'+export_line
                                                                    print(export_line)
                                                            for _, hit in range_table.iterrows():
                                                                    q_end = hit['q. end']
                                                                    gap = len(my_seq) - q_end
                                                                    s_end = hit['s. end']
                                                                    is_for = hit[fh_head]
                                                                    if is_for:
                                                                            if seq_borders[my_range][0] < my_range.get_min():
                                                                                    seq_borders[my_range][0] = s_end
                                                                                    seq_primers[my_range][0] = primer
                                                                                    if gap > 0:
                                                                                            vprint("Warning: sequencing primer does not match template at 3' end. Sequence probably needs trimming on the low end: {}".format(my_seq.id))
                                                                                    
                                                                            else:
                                                                                    if seq_borders[my_range][0] > s_end:
                                                                                            seq_borders[my_range][0] = s_end
                                                                                            seq_primers[my_range][0] = primer	
                                                                                            if gap > 0:
                                                                                                    vprint("Warning: sequencing primer does not match template at 3' end. Sequence probably needs trimming on the low end: {}".format(my_seq.id))	
                                                                                    vprint("Warning: multiple sequencing primers map in forward direction on template. Using outermost site: {}".format("-".join([locus,'Seq',subregion,seq_primers[my_range][0]])))
                                                                    else:
                                                                            if seq_borders[my_range][1] > my_range.get_max():
                                                                                    seq_borders[my_range][1] = s_end
                                                                                    seq_primers[my_range][1] = primer
                                                                                    if gap > 0:
                                                                                            vprint("Warning: sequencing primer does not match template at 3' end. Sequence probably needs trimming on the high end: {}".format(my_seq.id))
                                                                            else:
                                                                                    if seq_borders[my_range][1] < s_end:
                                                                                            seq_borders[my_range][1] = s_end																		
                                                                                            seq_primers[my_range][1] = primer
                                                                                            if gap > 0:
                                                                                                    vprint("Warning: sequencing primer does not match template at 3' end. Sequence probably needs trimming on the high end: {}".format(my_seq.id))
                                                                                    vprint("Warning: multiple sequencing primers map in reverse direction on template. Using outermost site: {}".format("-".join([locus,'Seq',subregion,seq_primers[my_range][1]])))
                                                    else: 
                                                            print("Warning: sequencing primer failed to map within PCR primers: {}".format(my_seq.id))
                                                    ## Record best hits for reporting
                                                    best_table = blast_table[blast_table['bit score'] >= best_in_range['bit score']] #This may be too stringent; may need to revisit
                                                    #~ print("Identified {} hits above threshold used for best in range".format(len(best_table)))
                                                    blast_combined = pd.concat([blast_combined,best_table],sort=True) ##Note: this is compatible with pandas 0.23 +; older versions will fail.
                                            else:
                                                    print("Warning: sequencing primer does not map to within PCR product. Exporting all matches for {}".format(my_seq.id))
                                                    blast_combined = pd.concat([blast_combined,blast_table],sort=True) ##Note: this is compatible with pandas 0.23 +; older versions will fail.
                    ##Export sequencing start sites
                    basename = locus
                    if subregion != 'All':
                        basename += '_' + subregion
                    for my_range in range_list:
                        if my_range in seq_primers: 
                            name = basename
                            name += '_{}_{}_{}'.format(seq_primers[my_range][0],seq_primers[my_range][1],os.path.basename(os.path.splitext(blast_db)[0])) ##Convoluted way to get the genome name
                            export_regions[locus][subregion][name] = {'contig':my_range.contig,'start':seq_borders[my_range][0]+1,'stop':seq_borders[my_range][1]-1}
                        else: ##seq_primers never got initialized because there is no match.
                            print("Notice: No sequencing primers for {} mapped with in the defined range for {}.".format(subregion,locus))
                    #I could add a way to orient the sequences (identify a reference primer)
            export_regions[locus]['OuterRange'] = range_list
        os.remove(temp_infile)
        os.remove(temp_outfile)
        if outfile != None:
                blast_combined.to_csv(outfile,index=False) ##columns=blast_default_headers+[ql_head,fh_head]
                export_line = 'Exported primer locations to '+outfile
    #             if __name__ != "__main__": ##Being called from an outside procedure...indent to indicated subsidiary position
    #                 export_line = '\t'+export_line
                print(export_line)
    #     current_verbose = default_verbose
        return export_regions
        
    def finish(self,keep_temp=False):
        if self.amplicon_info_file is not None:
            utilities.safeOverwriteTable(self.amplicon_info_file,pd.DataFrame(data=self.amplicon_info_list),'tab',index=False)
        if keep_temp:
            copytree(self.tempDirObj.name,os.path.join(self.outDir,'temp'))
            
            
class region_record:
    limit = 5000 #primers more than 5kb apart are considered different regions
    
    def __init__(self,exclusive_contig=None,exclusive_start=None,exclusive_stop=None):
        self.bestHitCounter = 0
        self.For_list = []
        self.Rev_list = []
        self.contig = 'Not specified'
        if exclusive_contig != None:
                self.exclusive = True ##An exclusive range cannot expand
                if exclusive_start >= exclusive_stop:
                        raise Exception("Region definition must start before stop")
                self.contig = exclusive_contig
                self.For_list.append(exclusive_start)
                self.Rev_list.append(exclusive_stop)
        else:
                self.exclusive = False
                if (exclusive_start != None) or (exclusive_stop != None):
                        raise Exception("Cannot define an exclusive region without a contig name")
                            
    def __str__(self):
        Fcnt = len(self.For_list)
        Rcnt = len(self.Rev_list)
        minF = min(self.For_list) if Fcnt > 0 else "N/A"
        maxR = max(self.Rev_list) if Rcnt > 0 else "N/A"
        return ("Predefined Exclusive Search Range: {}\n"
                "Contig: {} \n"
                "Number of best hits: {}\n"
                "Number of forward hits: {}\n"
                "Number of reverse hits: {} \n"                
                "First forward hit: {} \n"
                "Last reverse hit: {} \n".format(self.exclusive,self.contig,self.bestHitCounter,Fcnt,Rcnt,minF,maxR))
            
    def __repr__(self):
        return "region_record with {} primers".format(len(self.For_list+self.Rev_list))
            
    
                            
    def try_add_primer(self,this_contig,start,is_forward,best):
        ##Test if it is a new range
        new = not self.exclusive and len(self.For_list) == 0 and  len(self.Rev_list) == 0 
        ##Test if it fits into an existing range
        success = False
        if new:
                self.contig = this_contig
                success = True
        elif (this_contig == self.contig): #must be on same contig for starters
                full_list = self.For_list + self.Rev_list
                min_limit = min(full_list) 
                max_limit = max(full_list)
                if not self.exclusive: ##An exclusive range cannot expand
                        min_limit -= region_record.limit
                        max_limit += region_record.limit
                success = (start > min_limit) and (start < max_limit) 
        ##Add primer if it fits into range
        if success:
                if best:
                        self.bestHitCounter += 1
                if is_forward:
                        self.For_list.append(start)
                else:
                        self.Rev_list.append(start) 
        return success
            
    def try_merge_regions(self,other):
        if self.exclusive or other.exclusive:
            raise Exception("Exclusive ranges should never coexist with others")
        full_list = self.For_list + self.Rev_list
        min_limit = min(full_list) 
        max_limit = max(full_list)
        min_limit -= region_record.limit #could store the value
        max_limit += region_record.limit
        other_all = other.For_list + other.Rev_list
        other_min = min(other_all)
        other_max = max(other_all)
        success = (self.contig == other.contig
                    and (((other_max > min_limit) and (other_max < max_limit))  #other max is inside limits
                            or ((other_min > min_limit) and (other_min < max_limit)) # other_min is inside limits
                            or ((other_min < min_limit) == (other_max > max_limit)) # or one stradles the other
                            ))
        if success:
                self.For_list.extend(other.For_list)
                self.Rev_list.extend(other.Rev_list)
        return success
    
    #Test that list is not empty before calling
    def get_min(self):
        return min(self.For_list)
            
    def get_max(self):
        return max(self.Rev_list)

                
                        
                        
##Locate primers on genome, and extract the sequenced regions from within the amplicons

##This will fail if it is given funny genome filenames (spaces, etc)
import argparse
def main():
    ### Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--primer_file',help='Location of primer information',required=True)
    parser.add_argument('-r','--repository',help='Location of genome assembly repository')
    parser.add_argument('--keep_temp',action='store_true',help='Keep temporary BLAST files')
    parser.add_argument('--version','-V',action='version',version='%(prog)s {}.{}'.format(script_version,script_subversion))
    parser.add_argument('args', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    argv = [os.path.basename(__file__)] + args.args  
#     stdout = utilities.Logger(os.path.join(_outDir,"LocusExtractor.log"))
    repository = None
    default_settings = os.path.join(os.path.dirname(__file__),genomeOrganizer.SETTING_FILE)
    if args.repository:
        repository = args.repository  
    gd = genomeOrganizer.placeAssembliesIntoDataFrame(argv,GO_settings=default_settings,repository=repository)
    if gd is not None:
        primer_file = args.primer_file
        extractor = AmpliconExtractor(primer_file,generate_output=True)
        logFile = os.path.join(extractor.outDir,"AmpliconExtractor.log") if extractor.outDir is not None else "AmpliconExtractor.log" ##TODO find a better default location
        sys.stdout = utilities.Logger(logFile)
        if extractor.outDir is not None:
            utilities.safeOverwriteTable(genomeOrganizer.default_list(extractor.outDir), gd, 'tab')        
        for _,row in gd.iterrows():
            (file_format,compressed) = utilities.guessFileFormat(row.loc['Filename'])
            extractor.evaluateGenome(row.loc['Lab_ID'],row.loc['Filename'],file_format,compressed,keep_temp=args.keep_temp)
##    If I have to sort the columns somewhat (from LocusExtractor -- should be a function)
#     cols = self.allele_table_columns_initial + [c.strip() for c in column_order if c not in self.allele_table_columns_initial]
#     remainder = [c.strip() for c in self.allele_table.columns.tolist() if c not in cols]
#     remainder.sort(key=lambda s: s.lower())
#     cols += remainder            
        extractor.finish(keep_temp=args.keep_temp)
        print("Finished. Results saved at {}".format(extractor.outDir))
                
                    
if __name__ == "__main__":
    if not utilities.has_preferred_python():
        raise Exception("Upgrade your python version")
    main()
                

        




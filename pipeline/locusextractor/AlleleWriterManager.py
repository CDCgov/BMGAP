import utilities
import os
from Bio import Seq, SeqRecord, SeqIO
import shutil

###############################################################3
#
# This manages multiple sequence files for writing alleles to
#
#
#

class AlleleWriterManager():
    def __init__(self,out_directory,file_identifiers,output_basename='alleles.fasta'):
        assert isinstance(out_directory,str)
        assert isinstance(file_identifiers,set)
        assert isinstance(out_directory,str)
        self.directory = utilities.safeMakeOutputFolder(out_directory) ##Tacks on timestamp // safeMakeDir does not
        self.ids = file_identifiers
        self.basename = output_basename
        self.sequence_files = dict()
        for locus in self.ids:
            filename = os.path.join(self.directory,'{}_{}'.format(locus,self.basename))
            self.sequence_files[locus] = utilities.checkForOverwrite(filename) ## Will not overwrite file
            
    def writeToFile(self,locus,seq,name=''): ##TODO: add traslation feature
        if isinstance(seq,SeqRecord.SeqRecord):
            sr = seq
        else:
            if not isinstance(seq,Seq.Seq) or not isinstance(name,str):
                raise ValueError("Failed to write allele to output file")
            sr = SeqRecord.SeqRecord(seq,id=name, name=name, description='')
        out_file = self.sequence_files[locus]
        with open(out_file,"a") as fout:
            SeqIO.write(sr,fout,'fasta')
        if "phred_quality" in sr.letter_annotations:
            fastq_file = utilities.setExt(out_file, '.fastq', False)
            with open(fastq_file,'a') as fastq_out:
                SeqIO.write(sr,fastq_out,'fastq') #TODO - this should work with repository
        return sr
    
    def deleteFiles(self):
        shutil.rmtree(self.directory)
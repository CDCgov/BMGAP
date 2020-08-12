import sys
sys.path.append('..')
from AlleleWriterManager import AlleleWriterManager
import unittest
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio import SeqIO 
import os

class seq_utilitiesTest(unittest.TestCase):

    def setUp(self):
        
        self.s1 = 'GACTAGACTTAGT'
        self.s2 = 'GACTATAACTTAATATAG'
        self.s3 = 'GACTATAACTTAATATAC'
        self.seq1 = Seq(self.s1)
        self.seq2 = Seq(self.s2)
        self.seq3 = Seq(self.s3)
        self.sr1 = SeqRecord(self.seq1)
        self.sr2 = SeqRecord(self.seq2)
        self.sr3 = SeqRecord(self.seq3)
        self.fastq2 = SeqRecord(self.seq2,"test",letter_annotations = {"phred_quality":[1,2,4,10,20,25,33,22,33,35,18,11,23,8,2,1,2,0]})


    def test_fastq(self):
        writer = AlleleWriterManager("WriterTests",set(['a','b','c']))
        writer.writeToFile('a',self.fastq2)
        fasta_name = os.path.join(writer.directory,"a_alleles.fasta")
        self.assertTrue(os.path.exists(fasta_name),"Cannot find {}".format(os.path.abspath(fasta_name)))
        with open(fasta_name) as fin:
            seqs = SeqIO.to_dict(SeqIO.parse(fin,'fasta'))
        self.assertEqual(len(seqs),1, "Should have a single sequence in {}".format(fasta_name))
        fastq_name = os.path.join(writer.directory,"a_alleles.fastq")
        self.assertTrue(os.path.exists(fastq_name),"Cannot find {}".format(os.path.abspath(fastq_name)))
        with open(fastq_name) as fin:
            seqs = SeqIO.to_dict(SeqIO.parse(fin,'fastq'))
        self.assertEqual(len(seqs),1, "Should have a single sequence in {}".format(fastq_name))
        writer.deleteFiles()

#         
    def test_multi(self):
        writer = AlleleWriterManager("WriterTests",set(['a','b','c'])) ##Needs to write to a different folder
        writer.writeToFile('a',self.seq1,name='seq1')
        writer.writeToFile('a',self.seq2,name='seq2')
        fasta_name = os.path.join(writer.directory,"a_alleles.fasta")
        self.assertTrue(os.path.exists(fasta_name),"Cannot find {}".format(os.path.abspath(fasta_name)))
        with open(fasta_name) as fin:
            seqs = SeqIO.to_dict(SeqIO.parse(fin,'fasta'))
        self.assertEqual(len(seqs),2, "Should have two sequences in {}".format(fasta_name))
        writer.deleteFiles()        
#         
#     def test_trimFASTQ(self):
#         trimmed = trimFASTQtoFirstBase(self.fastq2, 10)
#         self.assertEqual(self.seq2.find(trimmed.seq),3,"Left trim is wrong 1")
#         self.assertEqual(self.seq2.reverse_complement().find(trimmed.seq.reverse_complement()),5,"Right trim in wrong")
#         trimmed = trimFASTQtoFirstBase(self.fastq2, 40)
#         self.assertEquals(trimmed,None,"Sequence should be discarded")
#         trimmed = trimFASTQtoFirstBase(self.fastq2, 22)
#         self.assertEqual(self.seq2.find(trimmed.seq),5,"Left trim is wrong 2")
#         self.assertEqual(self.seq2.reverse_complement().find(trimmed.seq.reverse_complement()),5,"Right trim in wrong")        
#         trimmed = trimFASTQtoFirstBase(self.fastq2, 23)
#         self.assertEqual(self.seq2.find(trimmed.seq),5,"Left trim is wrong 3")
#         self.assertEqual(self.seq2.reverse_complement().find(trimmed.seq.reverse_complement()),5,"Right trim in wrong")
#         trimmed = trimFASTQtoFirstBase(self.fastq2, 35)
#         self.assertEqual(len(trimmed),1,"trimmed too long")
#         self.assertEqual(trimmed[0],self.fastq2[10],"Wrong base recovered")
    
        
if __name__ == '__main__':
    unittest.main()
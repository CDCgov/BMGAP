import sys
sys.path.append('..')
from seq_utilities import find_first_stop, trim_at_first_stop, trimFASTQtoFirstBase, internal_stop, unambiguous_sequence
import unittest
from Bio.Seq import Seq
from Bio.SeqRecord import  SeqRecord

class seq_utilitiesTest(unittest.TestCase):

    def setUp(self):
        self.s1 = 'GACTAGACTTAGT'
        self.s2 = 'GACTATAACTTAATATAG'
        self.s3 = 'GACTATAACTTAATATAC'
        self.s4 = 'GACTATAACTTAATAWAC'
        self.seq1 = Seq(self.s1)
        self.seq2 = Seq(self.s2)
        self.seq3 = Seq(self.s3)
        self.seq4 = Seq(self.s4)
        self.sr1 = SeqRecord(self.seq1)
        self.sr2 = SeqRecord(self.seq2)
        self.sr3 = SeqRecord(self.seq3)
        self.sr4 = SeqRecord(self.seq4)
        self.fastq2 = SeqRecord(self.seq2,letter_annotations = {"phred_quality":[1,2,4,10,20,25,33,22,33,35,18,11,23,8,2,1,2,0]})


    def test_find(self):
        self.assertEqual(find_first_stop(self.s1),3,"Misplaced stop codon")
        self.assertEqual(find_first_stop(self.seq1),3,"Misplaced stop codon in seq1: "+str(self.seq1))
        self.assertEqual(find_first_stop(self.sr1),3,"Misplaced stop codon")
        self.assertTrue(internal_stop(self.s1))
        self.assertEqual(find_first_stop(self.s2),15,"Misplaced stop codon")
        self.assertEqual(find_first_stop(self.seq2),15,"Misplaced stop codon in seq2: "+str(self.seq2))
        self.assertEqual(find_first_stop(self.sr2),15,"Misplaced stop codon")
        self.assertFalse(internal_stop(self.seq2))
        self.assertEqual(find_first_stop(self.s3),None,"Misplaced stop codon")
        self.assertEqual(find_first_stop(self.seq3),None,"Misplaced stop codon in seq3: "+str(self.seq3))
        self.assertEqual(find_first_stop(self.sr3),None,"Misplaced stop codon")
        self.assertFalse(internal_stop(self.sr3))
        
    def test_trimORF(self):
        t1 = 'GAC'
        self.assertEqual(trim_at_first_stop(self.s1),t1,"Misplaced stop codon")
        self.assertEqual(trim_at_first_stop(str(self.seq1)),t1,"Misplaced stop codon in seq1: "+str(self.seq1))
        self.assertEqual(trim_at_first_stop(str(self.sr1.seq)),t1,"Misplaced stop codon")
        t2 = 'GACTATAACTTAATA'
        self.assertEqual(trim_at_first_stop(self.s2),t2,"Misplaced stop codon")
        self.assertEqual(trim_at_first_stop(str(self.seq2)),t2,"Misplaced stop codon in seq1: ")
        self.assertEqual(trim_at_first_stop(str(self.sr2.seq)),t2,"Misplaced stop codon")
        t3 = 'GACTATAACTTAATATAC'
        self.assertEqual(trim_at_first_stop(self.s3),t3,"Misplaced stop codon")
        self.assertEqual(trim_at_first_stop(str(self.seq3)),t3,"Misplaced stop codon in seq1: ")
        self.assertEqual(trim_at_first_stop(str(self.sr3.seq)),t3,"Misplaced stop codon")
        
    def test_trimFASTQ(self):
        trimmed = trimFASTQtoFirstBase(self.fastq2, 10)
        self.assertEqual(self.seq2.find(trimmed.seq),3,"Left trim is wrong 1")
        self.assertEqual(self.seq2.reverse_complement().find(trimmed.seq.reverse_complement()),5,"Right trim in wrong")
        trimmed = trimFASTQtoFirstBase(self.fastq2, 40)
        self.assertEquals(trimmed,None,"Sequence should be discarded")
        trimmed = trimFASTQtoFirstBase(self.fastq2, 22)
        self.assertEqual(self.seq2.find(trimmed.seq),5,"Left trim is wrong 2")
        self.assertEqual(self.seq2.reverse_complement().find(trimmed.seq.reverse_complement()),5,"Right trim in wrong")        
        trimmed = trimFASTQtoFirstBase(self.fastq2, 23)
        self.assertEqual(self.seq2.find(trimmed.seq),5,"Left trim is wrong 3")
        self.assertEqual(self.seq2.reverse_complement().find(trimmed.seq.reverse_complement()),5,"Right trim in wrong")
        trimmed = trimFASTQtoFirstBase(self.fastq2, 35)
        self.assertEqual(len(trimmed),1,"trimmed too long")
        self.assertEqual(trimmed[0],self.fastq2[10],"Wrong base recovered")
        
    def test_Ambig(self):
        self.assertTrue(unambiguous_sequence(self.s1))
        self.assertTrue(unambiguous_sequence(self.seq1))
        self.assertTrue(unambiguous_sequence(self.sr1))
        self.assertTrue(unambiguous_sequence(self.s2))
        self.assertTrue(unambiguous_sequence(self.seq2))
        self.assertTrue(unambiguous_sequence(self.sr2))
        self.assertTrue(unambiguous_sequence(self.s3))
        self.assertTrue(unambiguous_sequence(self.seq3))
        self.assertTrue(unambiguous_sequence(self.sr3))
        self.assertFalse(unambiguous_sequence(self.s4))
        self.assertFalse(unambiguous_sequence(self.seq4))
        self.assertFalse(unambiguous_sequence(self.sr4))
        
    
        
if __name__ == '__main__':
    unittest.main()
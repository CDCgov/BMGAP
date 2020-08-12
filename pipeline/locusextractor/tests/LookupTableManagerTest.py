import sys
import os
sys.path.append('..')

from LookupTableManager import LookupTableManager
import unittest

class TestTableManager(unittest.TestCase):

    def setUp(self):
        lookupDir = os.path.abspath('../lookupTables')
        self.tables = LookupTableManager(lookupDir)

    def test_sample(self):
        self.assertTrue(self.tables.lookup('fHbp','1','peptide_id') == '1')

if __name__ == '__main__':
    unittest.main()
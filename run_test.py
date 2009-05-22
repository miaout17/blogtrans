import unittest

import os

# Importers / Exporters
from blogtrans.wretch.WretchImporter import WretchImporter
from blogtrans.mt import *

from blogtrans.blogger.BloggerExporter import *
from blogtrans.blogger.BloggerImporter import *

class TestImporter(unittest.TestCase):
    def setUp(self):
        pass

    def test_wretch_import(self):
        path = "TestData/Wretch/"
        filenames = os.listdir(path)
        for filename in filenames :
            print "Parsing file %s" % filename
            importer = WretchImporter(path + filename)
            blogdata = importer.parse()

    def test_mt_import(self):
        path = "TestData/MT/"
        filenames = os.listdir(path)
        for filename in filenames :
            print "Parsing file %s" % filename
            importer = MTImporter(path + filename)
            blogdata = importer.parse()

            
# Todo: put really unittest in....
def main() :
    unittest.main()

if __name__ == "__main__" :
    main()

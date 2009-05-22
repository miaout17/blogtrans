import unittest

import os

# Importers / Exporters
from blogtrans.wretch.WretchImporter import WretchImporter
from blogtrans.mt import *

from blogtrans.blogger.BloggerExporter import *
from blogtrans.blogger.BloggerImporter import *

# Todo: better testcase structure
"""
class TestImporter(unittest.TestCase):
    def setUp(self):
        pass

    def test_wretch_import(self) :
        path = "TestData/Wretch/"
        filenames = os.listdir(path)
        for filename in filenames :
            print "Parsing file %s" % filename
            importer = WretchImporter(path + filename)
            blogdata = importer.parse()

    def test_mt_import(self) :
        path = "TestData/MT/"
        filenames = os.listdir(path)
        for filename in filenames :
            print "Parsing file %s" % filename
            importer = MTImporter(path + filename)
            blogdata = importer.parse()
    
    
    def test_blogger_import(self) :
        path = "TestData/Blogger/"
        filenames = os.listdir(path)
        for filename in filenames :
            print "Parsing file %s" % filename
            importer = WretchImporter(path + filename)
            blogdata = importer.parse()
    """

def test_wretch_import(filename) :
    #print "Parsing file %s" % filename
    importer = WretchImporter(filename)
    blogdata = importer.parse()

def main() :
    
    suite = unittest.TestSuite()
    
    path = "TestData/Wretch/"
    filenames = os.listdir(path)
    
    for filename in filenames :
        filename = path + filename
        func = lambda filename=filename: test_wretch_import(filename)
        case = unittest.FunctionTestCase( func, description = filename)
        suite.addTest(case)
    
    unittest.TextTestRunner(verbosity=2).run(suite)

    
    #case = unittest.FunctionTestCase

if __name__ == "__main__" :
    main()

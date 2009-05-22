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

def _make_import_testcase(importer_name, filename, path) :
    importer_class = globals()["%sImporter" % importer_name]
    def func() :
        full_filename = path + filename
        importer = importer_class(full_filename)
        blogdata = importer.parse()
    
    return unittest.FunctionTestCase(func, description="Import %s : %s" % (importer_name, filename) )
    
def make_import_testcases(importer_name) :
     
    path = "TestData/%s/" % importer_name
    cases = []
    filenames = os.listdir(path)
    for filename in filenames :
        cases.append( _make_import_testcase(importer_name, filename, path) )
    
    return cases
    
def main() :
    
    suite = unittest.TestSuite()

    suite.addTests( make_import_testcases("Wretch") )
    suite.addTests( make_import_testcases("MT") )
    suite.addTests( make_import_testcases("Blogger") )
    
    unittest.TextTestRunner(verbosity=2).run(suite)

    
    #case = unittest.FunctionTestCase

if __name__ == "__main__" :
    main()

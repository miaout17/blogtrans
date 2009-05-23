import unittest

import os
import random

# Importers / Exporters
from blogtrans.wretch.WretchImporter import WretchImporter
from blogtrans.mt import *

from blogtrans.blogger.BloggerExporter import *
from blogtrans.blogger.BloggerImporter import *

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
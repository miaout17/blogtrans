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

class TestStripXML(unittest.TestCase):

    @staticmethod
    def _is_valid_char(c) :
        val = ord(c)
        if val == 0x9 or val == 0xA or val == 0xD :
            return True
        elif val >= 0x20 and val <= 0xD7FF :
            return True
        elif val >= 0xE000 and val <= 0xFFFD :
            return True
        elif val >= 0x10000 and val <= 0x10FFFF :
            return True
        return False

    @staticmethod
    def _gen_string() :
        STR_LEN = 2000
        #slow here....refactoring?
        str = u""
        
        valid = 0
        invalid = 0
        
        for i in xrange(0, STR_LEN) :
            val = random.randint(1, 0x9999)
            c = unichr(val)
            if TestStripXML._is_valid_char(c) :
                valid += 1
            else :
                invalid += 1
            str += c
        #print "%d/%d" %(valid, invalid)
        return str

    def test_strip(self) :
        from blogtrans.util.XMLStripper import strip_xml, old_strip_xml
        
        for i in xrange(0, 20) :
            str = self._gen_string()
            self.assertEqual( strip_xml(str), old_strip_xml(str) )
            
    
def main() :
    
    suite = unittest.TestSuite()

    suite.addTest( TestStripXML("test_strip") )
    suite.addTests( make_import_testcases("Wretch") )
    suite.addTests( make_import_testcases("MT") )
    suite.addTests( make_import_testcases("Blogger") )
    
    unittest.TextTestRunner(verbosity=2).run(suite)

    
    #case = unittest.FunctionTestCase

if __name__ == "__main__" :
    main()

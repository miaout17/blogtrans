import unittest

import os
import random

from blogtrans.test import *
    
def main() :
    
    suite = unittest.TestSuite()

    suite.addTest( StripXMLTest("test_strip") )
    suite.addTests( make_import_testcases("Wretch") )
    suite.addTests( make_import_testcases("MT") )
    suite.addTests( make_import_testcases("Blogger") )
    
    unittest.TextTestRunner(verbosity=2).run(suite)
    
    #case = unittest.FunctionTestCase

if __name__ == "__main__" :
    main()

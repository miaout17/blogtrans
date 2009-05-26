import unittest

import os
import random

from blogtrans.test import *

import psyco
psyco.full()
    
def main() :
    suite = unittest.TestSuite()

    suite.addTest( StripXMLTest.StripXMLTest("test_strip") )
    suite.addTests( ImportExportTest.make_testcases() )
    
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__" :
    main()

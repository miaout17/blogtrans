import unittest

import os
import random

from blogtrans.test import *

try:
    import psyco
    psyco.full()
    print "Using psyco"
except ImportError:
    print "Failed to load psyco"

def main() :
    suite = unittest.TestSuite()

    suite.addTest( StripXMLTest.StripXMLTest("test_strip") )
    suite.addTests( ImportExportTest.make_testcases() )

    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__" :
    main()

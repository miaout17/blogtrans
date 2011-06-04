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

    def load_case(klass) :
        suite.addTests( unittest.TestLoader().loadTestsFromTestCase(klass) )

    suite.addTests( ImportExportTest.make_testcases() )
    load_case(StripXMLTest.StripXMLTest)
    load_case(WretchImporterTest.WretchImporterTest)

    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__" :
    main()

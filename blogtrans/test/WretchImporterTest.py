import unittest

from blogtrans.wretch.WretchImporter import WretchImporter
from datetime import datetime

class WretchImporterTest(unittest.TestCase):
    def test_parse_date(self) :
        assert datetime(2007,9,15,13,7)==WretchImporter.parse_date("2007-09-15 13:07:00")

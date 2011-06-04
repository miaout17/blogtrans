import unittest
import random
from blogtrans.util.XMLStripper import strip_xml, old_strip_xml

class StripXMLTest(unittest.TestCase):

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
            if StripXMLTest._is_valid_char(c) :
                valid += 1
            else :
                invalid += 1
            str += c
        #print "%d/%d" %(valid, invalid)
        return str

    def test_strip(self) :

        for i in xrange(0, 20) :
            str = self._gen_string()
            self.assertEqual( strip_xml(str), old_strip_xml(str) )


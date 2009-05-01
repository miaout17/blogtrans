from StringIO import StringIO

def strip_xml(source) :
    sio = StringIO(u"")

    for c in source :
        val = ord(c)
        valid = False
        if val == 0x9 or val == 0xA or val == 0xD :
            valid = True
        elif val >= 0x20 and val <= 0xD7FF :
            valid = True
        elif val >= 0xE000 and val <= 0xFFFD :
            valid = True
        elif val >= 0x10000 and val <= 0x10FFFF :
            valid = True
            
        if valid :
            sio.write(c)
        #    result += c

    return sio.getvalue()

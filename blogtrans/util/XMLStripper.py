from StringIO import StringIO

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

def strip_xml(source) :
    sio = StringIO(u"")

    last_proceed = -1
    current = 0

    while current < len(source) :
        c = source[current]
        if not _is_valid_char(c) :
            if last_proceed != current - 1 :
                sio.write( source[ (last_proceed+1) : current ] )
            last_proceed = current
        current += 1
    sio.write( source[ (last_proceed+1) : current ] )

    return sio.getvalue()

def old_strip_xml(source) :
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

    return sio.getvalue()

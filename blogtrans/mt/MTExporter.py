import codecs

import sys
from datetime import datetime

from blogtrans.data import *

class MTExporter :
    def __init__(self, filename, blogdata) :
        self.filename = filename
        self.blogdata = blogdata

    def Export(self) :
        #f = open(self.filename,"w")
        f = codecs.open(self.filename, "w", encoding="utf-8")
        for a in self.blogdata.articles :
            f.write(u"AUTHOR: %s\n" % a.author)
            f.write(u"TITLE: %s\n" % a.title)
            f.write(u"DATE: %s\n" % a.date.strftime("%m/%d/%y %I:%M:%S %p"))
            for i, v in enumerate(a.category):
                if i==0 :
                    f.write(u"PRIMARY CATEGORY: %s\n" % v)
                else :
                    f.write(u"CATEGORY: %s\n" % v)
            if a.status == Article.PUBLISH : status_text = "publish"
            else : status_text = "draft"
            f.write(u"STATUS: %s\n" % status_text)
            f.write(u"-----\n")
            f.write(u"BODY: \n")
            f.write(a.body)
            f.write(u"\n-----\n")
            if (a.extended_body != "") :
                f.write(u"EXTENDED BODY: \n")
                f.write(a.extended_body)
                f.write(u"\n-----\n")
            for c in a.comments :
                f.write(u"COMMENT:\n")
                f.write(u"AUTHOR: %s\n" % c.author)
                f.write(u"DATE: %s\n" % c.date.strftime("%m/%d/%y %I:%M:%S %p"))
                f.write(u"%s" % c.body)
                f.write(u"\n-----\n")
            f.write(u"\n--------\n")
        f.close

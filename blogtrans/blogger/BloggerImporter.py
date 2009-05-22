import codecs

import xml.etree.ElementTree as ET

from datetime import datetime

from blogtrans.data import *

class BloggerImporter :
    def __init__(self, filename) :
        self.filename = filename
        
    def parse(self) :
        blogdata = BlogData()
        f = codecs.open(self.filename, "r")
        xml_data = f.read()
        f.close()
        
        tree = ET.fromstring(xml_data)
        for entry in tree.findall("entry") :
            print entry
        
        """
    self.author = ""
    self.title = ""
    self.date = datetime.today()
    self.category = []
    self.status = Article.PUBLISH
    self.allow_comments = True
    self.allow_pings = True
    #self.convert_breaks = True

    self.body = ""
    self.extended_body = ""
    self.excerpt = ""

    self.comments = []
    self.pings = []"""
        
        return blogdata
        


 

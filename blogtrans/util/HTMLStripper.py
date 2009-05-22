from HTMLParser import HTMLParser
import urllib

#strip every tags from html code
class StripParser(HTMLParser):
    def __init__(self) :
        HTMLParser.__init__(self)
        self.output = ""

    def handle_starttag(self, tag, attrs):
        print "Encountered the beginning of a %s tag" % tag

    def handle_endtag(self, tag):
        print "Encountered the end of a %s tag" % tag
        
    def handle_startendtag(self, tag, attrs) :
        print "Encountered a empty tag %s " % tag
        
    def handle_data(self, data) :
        self.output += data 

    def handle_charref(self, name) :
        self.output += "&#%s;" % name

    def handle_entityref(self, name) :
        #TODO: check if this is Okay
        self.output += "&%s" % name

    #def handle_comment(self, data) :
    #def handle_decl(self, decl) :
    #def handle_pi(self, data) :

def StripHTML(data) :
    parser = StripParser()
    parser.feed(data)
    parser.close()
    return parser.output
    
#print StripHTML(urllib.urlopen("http://www.google.com").read())

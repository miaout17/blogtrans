from blogtrans.ui.MainWindow import *
import sys, traceback
import getopt
import wx

# Importers / Exporters
from blogtrans.wretch.WretchImporter import WretchImporter
from blogtrans.mt import *

from blogtrans.blogger.BloggerExporter import *
from blogtrans.blogger.BloggerImporter import *


def trap_error(func) :
    def f() :
        try:
            func()
        except Exception, inst :
            type, value, tb = sys.exc_info()
            print "\n".join(traceback.format_exception(type, value, tb))
            raw_input()
    return f

@trap_error
def main() : 
    long_opts = [ "import-wretch=" ]
    opts, args = getopt.getopt(sys.argv[1:], "n", long_opts)
   
    no_window = False
    
    for o, a in opts :
        if o=="-n" :
            no_window = True
        if o=="--import-wretch" :
            blogdata = WretchImporter(a).parse()
            print blogdata.GetArticleCount()

    if not no_window :
        app = wx.PySimpleApp()
        frame=MainWindow()
        app.MainLoop()

if __name__ == "__main__" :
    main()

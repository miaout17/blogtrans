from blogtrans.ui.MainWindow import *
import sys, traceback
import wx

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
    app = wx.PySimpleApp()
    frame=MainWindow()
    app.MainLoop()

main()

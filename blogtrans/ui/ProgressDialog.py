# coding=big5

import wx._core as wx
from threading import *
import sys, traceback

ID_BREAK = wx.NewId()
ID_CLOSE = wx.NewId()

class ProgressDialog(wx.Dialog) :
    RUNNING = 1
    BREAK = 2
    FINISH = 3
    FAIL = 4

    def __init__(self, parent) :
        wx.Dialog.__init__(self, parent, style=wx.CAPTION) #, style=wx.OK|wx.CANCEL|wx.CENTRE) #, style=wx.CAPTION

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)

        self.textctrl = wx.TextCtrl(self, 1, style=wx.TE_MULTILINE)
        self.textctrl.SetEditable(False)

        self.break_button = wx.Button(self, ID_BREAK, "中斷操作")
        self.close_button = wx.Button(self, ID_CLOSE, "關閉視窗")
        self.close_button.Enable(False)

        wx.EVT_BUTTON(self, ID_CLOSE, self.OnClose)
        wx.EVT_BUTTON(self, ID_BREAK, self.OnBreak)

        self.sizer2.Add(self.break_button, 1, wx.FIXED_MINSIZE)
        self.sizer2.Add(self.close_button, 1, wx.FIXED_MINSIZE)

        self.sizer.Add(self.textctrl, 1, wx.EXPAND)
        self.sizer.Add(self.sizer2,0,wx.EXPAND)

        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)

        self.Bind(wx.EVT_CLOSE, self.HandleClose)

        self.status = self.RUNNING
        self.user_break = False

        thread = Thread()
        thread.run = self.Run

        thread.start()

    def OnClose(self, e) :
        self.Close(True)

    def OnBreak(self, e) :
        self.user_break = True

    def HandleClose(self, e) :
        if self.status != self.RUNNING :
            self.Destroy()
        else :
            print "Processing....Can't close the window"

    def ChangeButtonStatus(self) :
        self.close_button.Enable(True)
        self.break_button.Enable(False)

    def Print(self, str) :
        self.textctrl.AppendText(str+"\n")

    def Run(self) :
        #Todo: ERROR Handling HERE!!!!!! .... Catch exception!!!!!
        try:
            self._Run()
        except Exception, inst :
            type, value, tb = sys.exc_info()
            self.Print("\n".join(traceback.format_exception(type, value, tb)) )
            self.Print("發生錯誤!!")

        if self.status == self.FAIL :
            pass
        else :
            if self.user_break :
                self.status = self.BREAK
            else :
                self.status = self.FINISH
        self.ChangeButtonStatus()

    def _Run(self) :
        #This is a example run func....
        #Override this function!!
        i = 0
        while i < 100000 :
            self.Print("%i\n"%i)
            i += 1
            if self.user_break : break






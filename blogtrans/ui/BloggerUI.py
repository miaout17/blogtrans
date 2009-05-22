# coding=big5

# Deprecated after Rev15
import wx._core as wx

from blogtrans.blogger.blogger import *
from ProgressDialog import ProgressDialog
import sys, traceback

ID_CANCEL = wx.NewId()
ID_OK = wx.NewId()
ID_AUTH = wx.NewId()

class BloggerExportProgress(ProgressDialog) :
    def __init__(self, parent, blogger, blogdata) :
        ProgressDialog.__init__(self, parent)
        
        self.blogger = blogger
        self.blogdata = blogdata
        
    def _Run(self) :
        try:
            for article in self.blogdata.articles :
                self.Print(u"正在匯出文章: %s" % article.title)
                
                if self.user_break : return
                post = self.blogger.CreatePost(article)
                
                self_id = post.id.text 
                tokens = self_id.split("-")
                article_id = tokens[-1]
                
                for comment in article.comments :
                    if self.user_break : return
                    self.Print(u"正在匯出留言: %s" % comment.author)
                    self.blogger.CreateComment(article_id, comment)
        except Exception, inst :
            type, value, tb = sys.exc_info()
            self.Print("\n".join(traceback.format_exception(type, value, tb)) )
            self.status = self.FAIL
            self.Print("無法上傳文章!!\n可能是由於超過每天50篇的限制")
            
        

class BloggerAuthUI(wx.Dialog) :

    def __init__(self, parent):
        wx.Dialog.__init__(self, None, wx.ID_ANY, "Blogger", size=(255, 365))

        vbox_top = wx.BoxSizer(wx.VERTICAL)
        vbox = wx.BoxSizer(wx.VERTICAL)

        panel1 = wx.Panel(self, -1)
        grid1 = wx.GridSizer(3, 2)
        
        grid1.Add(wx.StaticText(panel1, -1, '帳號(Email): ', (5, 5)), 0,    wx.ALIGN_CENTER_VERTICAL)
        self.email_ctrl = wx.TextCtrl(panel1, -1, size=(120, -1))
        grid1.Add(self.email_ctrl)
        
        grid1.Add(wx.StaticText(panel1, -1, '密碼: ', (5, 5)), 0, wx.ALIGN_CENTER_VERTICAL)
        self.password_ctrl = wx.TextCtrl(panel1, -1, size=(120, -1), style=wx.TE_PASSWORD)
        grid1.Add(self.password_ctrl)

        auth_button = wx.Button(panel1, ID_AUTH, '驗證Blogger')
        grid1.Add(auth_button, wx.EXPAND)
        wx.EVT_BUTTON(self, ID_AUTH, self.OnAuth)

        panel1.SetSizer(grid1)
        vbox.Add(panel1, 0, wx.BOTTOM | wx.TOP, 9)

        self.bloglist = wx.ListBox(self, -1)
        vbox.Add(self.bloglist, 1, wx.EXPAND)

        panel4 = wx.Panel(self, -1)
        sizer4 = wx.GridSizer(1, 2, 2, 2)
        
        button_ok = wx.Button(panel4, ID_OK, '開始匯出')
        button_close = wx.Button(panel4, ID_CANCEL, '取消並關閉')
        sizer4.Add(button_ok, wx.EXPAND)
        sizer4.Add(button_close, wx.EXPAND)
        
        wx.EVT_BUTTON(self, ID_CANCEL, self.OnCancel)
        wx.EVT_BUTTON(self, ID_OK, self.OnOK)

        panel4.SetSizer(sizer4)
        vbox.Add(panel4, 0, wx.BOTTOM, 9)

        vbox_top.Add(vbox, 1, wx.LEFT, 5)
        self.SetSizer(vbox_top)
    
    def OnCancel(self, e) :
        self.blogger = None
        self.Close()
        
    def OnOK(self, e) :
        selection = self.bloglist.GetSelection()
        if selection==-1 : return
        self.blogger.SelectBlog(selection)
        self.Close()

    def OnAuth(self, e) :
        self.bloglist.Clear()
        
        #TODO: error handling
        email = self.email_ctrl.GetValue()
        password = self.password_ctrl.GetValue()
        self.blogger = Blogger(email, password)
        print self.blogger
        
        for name in self.blogger.blognames :
            self.bloglist.Append(name)
        
        



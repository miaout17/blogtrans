# coding=big5

import copy, os
import wx._core as wx
from wx.html import HtmlWindow

from BlogTreeCtrl import BlogTreeCtrl
from BlogHtmlCtrl import BlogHtmlWindow
from ProgressDialog import *

from blogtrans.data import *
from blogtrans.wretch.WretchImporter import WretchImporter
from blogtrans.mt import *

from blogtrans.blogger.BloggerExporter import *

ID_IMPORT_WRETCH = wx.NewId()
ID_IMPORT_MT = wx.NewId()

ID_EXPORT_BLOGGER = wx.NewId()
ID_EXPORT_MT = wx.NewId()

class MainWindow(wx.Frame):

  def __init_menubar(self) :
  
    #Todo: use a smarter way to manage menu...
    import_menu = wx.Menu()
    
    import_menu.Append(ID_IMPORT_WRETCH, "無名XML檔案(&W)...","匯入無名XML檔案")
    wx.EVT_MENU(self, ID_IMPORT_WRETCH, self.OnImportWretch)
    
    import_menu.Append(ID_IMPORT_MT, "&MT檔案...","匯入MT Import檔案")
    wx.EVT_MENU(self, ID_IMPORT_MT, self.OnImportMT)
    
    export_menu = wx.Menu()
    export_menu.Append(ID_EXPORT_BLOGGER, "Blogger(&B)...","匯出至Blogger XML")
    wx.EVT_MENU(self, ID_EXPORT_BLOGGER, self.OnExportBlogger)

    export_menu.Append(ID_EXPORT_MT, "&MT檔案...","匯出至MT檔案")
    wx.EVT_MENU(self, ID_EXPORT_MT, self.OnExportMT)
    
    menuBar = wx.MenuBar()
    menuBar.Append(import_menu,"匯入(&I)")
    menuBar.Append(export_menu,"匯出(&E)")
     
    self.SetMenuBar(menuBar)

  def __init__(self) :
    wx.Frame.__init__(self, None, wx.ID_ANY, 'BlogTrans 部落格搬家工具 V0.1', size=(800,600))
    
    self.sizer = wx.BoxSizer(wx.HORIZONTAL)
    
    self.treectrl = BlogTreeCtrl(self)
    self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self.treectrl)    
    
    #self.textctrl = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_MULTILINE) 
    self.html = BlogHtmlWindow(self)
    
    self.sizer.Add(self.treectrl,1,wx.EXPAND)
    self.sizer.Add(self.html,2,wx.EXPAND)
    
    self.SetSizer(self.sizer)
    self.SetAutoLayout(1)
    
    self.__init_menubar()
    self.CreateStatusBar()
    
    #self.OnImportWretch(None)
    
    #self.sizer.Fit(self)
    self.Show(True)
    
  # TODO: Bad design here, takes O(n^2) time complexity....
  def GetCheckedBlogData(self) :
    checked = self.treectrl.GetAllCheckedData()
    
    data = BlogData()
    comment_count = 0

    for article in self.blogdata.articles :
      if article in checked :
        a = copy.deepcopy(article)
        data.articles.append(a)
        a.comments = []

        print len(article.comments)
        for comment in article.comments :
          if comment in checked :
            a.comments.append(comment)
            comment_count += 1
        
    print "Article: ", len(self.blogdata.articles), len(data.articles), len(checked)
    print "Comment: ", comment_count
    return data
    
  def setBlogData(self, blogdata) :
    self.blogdata = blogdata
    self.treectrl.setBlogData(blogdata)
    
  def OnImportWretch(self, e) :
    dialog = wx.FileDialog(self)
    result = dialog.ShowModal()
    dialog.Destroy()
    if result != wx.ID_OK :
      return
    else :
      file = dialog.GetFilename()
      dir = dialog.GetDirectory()
      filename = os.path.join(dir, file)
    
    wi = WretchImporter(filename)
    blogdata = wi.parse()
    self.setBlogData(blogdata)

  def OnImportMT(self, e) :
    dialog = wx.FileDialog(self)
    result = dialog.ShowModal()
    dialog.Destroy()
    if result != wx.ID_OK :
      return
    else :
      file = dialog.GetFilename()
      dir = dialog.GetDirectory()
      filename = os.path.join(dir, file)
      
    mi = MTImporter(filename)
    blogdata = mi.parse()
    self.setBlogData(blogdata)

  def OnExportMT(self, e) :
    checked_data = self.GetCheckedBlogData()
    dialog = wx.FileDialog(self, style=wx.SAVE|wx.OVERWRITE_PROMPT)
    result = dialog.ShowModal()
    dialog.Destroy()
    if result != wx.ID_OK :
      return
    else :
      file = dialog.GetFilename()
      dir = dialog.GetDirectory()
      filename = os.path.join(dir, file)
    me = MTExporter(filename, checked_data)
    me.Export()
    
  def OnExportBlogger(self, e) :
    checked_data = self.GetCheckedBlogData()
    dialog = wx.FileDialog(self, style=wx.SAVE|wx.OVERWRITE_PROMPT)
    result = dialog.ShowModal()
    dialog.Destroy()
    if result != wx.ID_OK :
      return
    else :
      file = dialog.GetFilename()
      dir = dialog.GetDirectory()
      filename = os.path.join(dir, file)
    me = BloggerExporter(filename, checked_data)
    me.Export()
    
  
  def OnSelChanged(self, e) :
    # Tofix:  seems a sync problem here
    data = e.GetItem().GetData()
    # print data.__class__
    if data.__class__ == Article :
      self.html.ShowArticle(data)
    elif data.__class__ == Comment :
      self.html.ShowComment(data)
    else :
      self.html.SetPage("")
  


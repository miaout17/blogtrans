# coding=big5
#from wx import *

import wx._core as wx
from wx.html import *
import string

from blogtrans.data import Article

def make_html_list(list) :
  str = "<ul>"
  for item in list :
    str += "<li>" + item + "</li>"
  str += "</ul>"
  str += "<hr />"
  return str

class BlogHtmlWindow(HtmlWindow):
  def __init__(self, parent) :
    HtmlWindow.__init__(self,parent,wx.ID_ANY, style = wx.SIMPLE_BORDER)
    
  def ShowArticle(self, article) :
    info = []
    
    info.append(u"作者: "+article.author )
    info.append(u"標題: "+article.title )
    info.append(u"日期: "+article.date.strftime("%Y-%m-%d %H:%M:%S") )
    info.append(u"類別: "+string.join(article.category, ",") )
    
    if article.status==Article.PUBLISH : status = u"公開"
    elif article.status==Article.DRAFT : status = u"草稿"
    else : status = u"私密"
    info.append(u"狀態: "+status)
    
    self.SetPage(make_html_list(info)+article.body+article.extended_body)
    
  def ShowComment(self, comment) :
    info = []
    
    info.append(u"留言者: " + comment.author )
    info.append(u"Email: " +comment.email )
    info.append(u"網址: " + comment.url)
    info.append(u"日期: " + comment.date.strftime("%Y-%m-%d %H:%M:%S") )
    
    self.SetPage(make_html_list(info)+comment.body)
    
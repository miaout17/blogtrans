# coding=big5

import wx._core as wx
from wx.lib.customtreectrl import *

class BlogTreeCtrl(CustomTreeCtrl) :
    def __init__(self, parent):
        #TR_MULTIPLE
        super(BlogTreeCtrl, self).__init__(parent, style=TR_HAS_BUTTONS|TR_TWIST_BUTTONS|TR_AUTO_CHECK_CHILD    )

    def GetAllCheckedData(self) :
        checked = []
    
        item = self.GetRootItem()
        item = self.GetNext(item)
        while item :
            #print item.GetData()
            if self.IsItemChecked(item):
                checked.append(item.GetData())
            item = self.GetNext(item)
            
        return set(checked)
        
    def setBlogData(self, blogdata) :
        self.DeleteAllItems()
        root = self.AddRoot('Blog')

        for article in blogdata.articles :
            article_item = self.AppendItem(root, article.title, ct_type=1, data=article)
            self.CheckItem(article_item)
            
            if len(article.comments)!=0 : self.SetItemHasChildren(article_item, True)            
            
            for comment in article.comments :
                #print comment.author
                comment_item = self.AppendItem(article_item, comment.author+u" 的回應", ct_type=1, data=comment)
                self.CheckItem(comment_item)
        self.Expand(root)
        
        
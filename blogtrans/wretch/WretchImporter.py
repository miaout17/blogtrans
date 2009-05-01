from blogtrans.data import *
import xml.etree.ElementTree as ET
from datetime import datetime

class WretchImporter :
  def __init__(self, filename) :
    self.filename = filename
    #f = codecs.open(self.filename, encoding="utf-8")
  
  def parse(self) :
  
    f = open(self.filename)
    xml_data = f.read()
    f.close()
    
    end_pattern = "</blog_backup>"
    end_index  = xml_data.rfind(end_pattern) + len(end_pattern)
    xml_data = xml_data[0:end_index]
    #tree = ET.parse(self.filename)
    tree = ET.fromstring(xml_data)
    
    category_nodes = tree.findall("blog_articles_categories/category")
    article_nodes = tree.findall("*/article")
    comment_nodes = tree.findall("blog_articles_comments/article_comment")
    #print "Count: ", len(article_nodes), len(comment_nodes)

    # mapping from article_id to Article object
    aid_map = {}
    cid_name = {}
	
    blogdata = BlogData()

    #Todo: error handling
    
    
    for node in category_nodes :
      cid = node.findtext("id")
      cname = node.findtext("name")
      cid_name[cid] = cname
    
    for node in article_nodes:
      article = Article()

      article.author = node.findtext("userid")
      article.title = node.findtext("title")
      article.date = datetime.strptime(node.findtext("PostTime"), "%Y-%m-%d %H:%M:%S")
      
      #In wretch, every article has  only 1 category
      cid = node.findtext("category_id")
      if cid in cid_name : 
        article.category.append(cid_name[cid])
      
      if node.findtext("isCloak") == "0" :
        article.status = Article.PUBLISH
      else :
        article.status = Article.PRIVATE
      
      article.allow_comments = True
      article.allow_pings = True

      article.body = node.findtext("text")

      aid = node.findtext("id")
      aid_map[aid] = article
      blogdata.articles.append(article)

    for node in comment_nodes:
      comment = Comment()

      comment.author = aid = node.findtext("name")
      comment.email = node.findtext("email")
      comment.url = node.findtext("url")
      comment.date = datetime.strptime(node.findtext("date"), "%Y-%m-%d %H:%M:%S")
      comment.body = aid = node.findtext("text")
      
      aid = node.findtext("article_id")
      article = aid_map[aid]
      article.comments.append(comment)
    
    #TODO: process category
    return blogdata

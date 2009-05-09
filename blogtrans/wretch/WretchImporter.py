from blogtrans.data import *
import xml.etree.ElementTree as ET
from datetime import datetime
from blogtrans.util.XMLStripper import strip_xml

def my_rfind(str, pattern) :
    pat_len = len(pattern) 
    if pat_len > len(str) : return -1
    
    for start_pos in range( len(str)-pat_len, -1, -1) :
        part = str[start_pos:start_pos+pat_len]
        if part==pattern :
            return start_pos
    return -1

class WretchImporter :
  def __init__(self, filename) :
    self.filename = filename
    #f = codecs.open(self.filename, encoding="utf-8")
  
  def parse(self) :
  
    f = open(self.filename, "rb")
    xml_data = f.read()
    f.close()
    print len(xml_data)
    xml_data = xml_data.decode("utf8", "replace")
    xml_data = strip_xml(xml_data)
    print len(xml_data)
    xml_data = xml_data.encode("utf8")
    print len(xml_data)
    
    end_pattern = "</blog_backup>"
    #find_index = xml_data.rfind(end_pattern)
    find_index = my_rfind(xml_data, end_pattern)
    
    end_index = find_index + len(end_pattern)
    print find_index
    
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
      try : 
        article = aid_map[aid]
        article.comments.append(comment)
      except KeyError :
        print "Comment %s missing article %s" % (cid, aid)
    
    #TODO: process category
    return blogdata

from datetime import *

class Article :
  PUBLISH = 0
  DRAFT = 1
  PRIVATE = 2
  
  def __init__(self) :
    self.author = ""
    self.title = ""
    self.date = datetime.today()
    self.category = []
    self.status = Article.PUBLISH
    self.allow_comments = True
    self.allow_pings = True
    #self.convert_breaks = True

    self.body = ""
    self.extended_body = ""
    self.excerpt = ""

    self.comments = []
    self.pings = []
    

# coding=big5

try:
  from xml.etree import ElementTree # for Python 2.5 users
except:
  from elementtree import ElementTree
from gdata import service
import gdata
import atom
import getopt
import sys

from datetime import datetime

from blogtrans.data import *
from blogtrans.util.HTMLStripper import StripHTML

class Blogger:
  def __init__(self, email, password):
    
    self.service = service.GDataService(email, password)
    self.service.source = 'BlogTrans'
    self.service.service = 'blogger'
    self.service.server = 'www.blogger.com'
    self.service.ProgrammaticLogin()

    query = service.Query()
    query.feed = '/feeds/default/blogs'
    feed = self.service.Get(query.ToUri())
    
    self.blogids = []
    self.blognames = []
    
    # Print the results.
    print feed.title.text
    for entry in feed.entry:
      blog_id = entry.GetSelfLink().href.split('/')[-1]
      blog_name = entry.title.text
      print blog_id+"\t" + blog_name
      self.blogids.append( blog_id )
      self.blognames.append( blog_name )
      
  def SelectBlog(self, n) :
    self.blog_id = self.blogids[n]

  def CreatePost(self, article):
  
    # Create the entry to insert.
    entry = gdata.GDataEntry()
    entry.author.append(atom.Author(atom.Name(text=article.author)))

    #timetext = article.date.strftime("%Y
    # to be modified    
    # entry.published = atom.Published(text="2006-11-08T18:10:00.000-08:00")
    # entry.updated = atom.Updated(text="2006-11-08T18:10:00.000-08:00")
    
    datetext = article.date.strftime("%Y-%m-%dT%I:%M:%S.000-08:00")
    entry.published = atom.Published(datetext)
    entry.updated = atom.Updated(datetext)
   
    entry.title = atom.Title(title_type='xhtml', text=article.title)
    for category_name in article.category :
      entry.category.append(atom.Category(scheme="http://www.blogger.com/atom/ns#", term=category_name))
    entry.content = atom.Content(content_type='html', text=article.body+article.extended_body)
    
    if article.status!=article.PUBLISH :
      control = atom.Control()
      control.draft = atom.Draft(text='yes')
      entry.control = control

    # Ask the service to insert the new entry.
    return self.service.Post(entry, '/feeds/' + self.blog_id + '/posts/default')

  def CreateComment(self, post_id, comment):
    # Build the comment feed URI
    feed_uri = '/feeds/' + self.blog_id + '/' + post_id + '/comments/default'

    # Create a new entry for the comment and submit it to the GDataService
    entry = gdata.GDataEntry()
    #atom.Author(atom.Name(text="Tester"))
    
    body = u"原作者: %s\n" % comment.author
    body += u"張貼時間: %s\n" % comment.date.strftime("%Y-%m-%dT%I:%M:%S.000-08:00")
    body += StripHTML(comment.body)
    
    entry.content = atom.Content(content_type='xhtml', text=body )
    return self.service.Post(entry, feed_uri)

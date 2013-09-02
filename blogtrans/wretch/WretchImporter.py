# coding=utf8
from blogtrans.data import *
import xml.etree.ElementTree as ET
from datetime import datetime
from blogtrans.util.XMLStripper import strip_xml
import re

DATETIME_RE = re.compile(r'^(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})$')

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

    def parse(self) :
        try :
            return self.__parse(False)
        except :
            self.log("嘗試清理XML格式再重新解析...")
            return self.__parse(True)

    @classmethod
    def log(self, message) :
        print message

    @classmethod
    def parse_date(self, date_str) :
        try:
            return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        except Exception as e:
            self.log("解析日期失敗：{}".format(date_str))
            raise e

    def __parse(self, preprocess) :

        f = open(self.filename, "rb")
        xml_data = f.read()
        f.close()

        if preprocess :
            xml_data = xml_data.decode("utf8", "replace")
            xml_data = strip_xml(xml_data)
            xml_data = xml_data.encode("utf8")

        end_pattern = "</blog_backup>"
        find_index = my_rfind(xml_data, end_pattern)

        end_index = find_index + len(end_pattern)

        xml_data = xml_data[0:end_index]
        tree = ET.fromstring(xml_data)

        category_nodes = tree.findall("blog_articles_categories/category")
        article_nodes = tree.findall("*/article")

        # Wretch uses blog_articles_comments_%d%d instead of blog_articles_comments now
        # where %d%d is 2-digit number. This correctly find all comments

        comment_nodes = tree.findall("*/article_comment")

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
            article.date = self.parse_date(node.findtext("date"))

            #In wretch, every article has only 1 category
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


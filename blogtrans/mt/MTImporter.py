# coding=utf8
import codecs

import re
from datetime import datetime

from blogtrans.data import *
import string

def parse_date(date_str) :

    #process informal situation
    date_str = string.replace(date_str, u"上午", u"AM")
    date_str = string.replace(date_str, u"下午", u"PM")

    if re.compile("\d\d/\d\d/\d\d\d\d").match(date_str) :
        try:
            return datetime.strptime(date_str, "%m/%d/%Y %I:%M:%S %p")
        except:
            return datetime.strptime(date_str, "%m/%d/%Y %H:%M:%S")
    try:
        return datetime.strptime(date_str, "%m/%d/%y %I:%M:%S %p")
    except:
        return datetime.strptime(date_str, "%m/%d/%y %H:%M:%S")


class MTImporter :
    def __init__(self, filename) :
        self.filename = filename
        self.entries = []
        self.blogdata = BlogData()

    def split_array(self, array, splitter) :
        result = []
        start = 0
        for i in range(0, len(array) ) :
            if array[i].strip() == splitter:
                result.append(array[start:i])
                start = i+1
        if start < len(array) :
            result.append(array[start:len(array)])
        return result

    def parse_comment(self, text) :
        comment = Comment()
        attr = set(["AUTHOR", "EMAIL", "URL", "IP", "DATE"])

        for i, v in enumerate(text):
            tmp = v.split(":", 1)
            key = tmp[0]
            if key in attr :
                value = tmp[1].strip()
                if key == "AUTHOR" :
                    comment.author = value
                elif key == "EMAIL" :
                    comment.email = value
                elif key == "URL" :
                    comment.url = value
                elif key == "IP" :
                    comment.ip = value
                elif key == "DATE" :
                    comment.date = parse_date(value)
            else :
                break

        comment.body = "".join(text[i:])

        return comment

    def parse_entry(self, text) :
        #entry = {}
        #entry["COMMENT"] = []
        article = Article()

        single_line = set(["AUTHOR", "TITLE", "DATE", "PRIMARY CATEGORY", "CATEGORY", "STATUS",
                                             "ALLOW COMMENTS", "ALLOW PINGS", "CONVERT BREAKS", "NO ENTRY"])
        multi_line = set(["BODY", "EXTENDED BODY", "EXCERPT", "COMMENT", "PING"])

        in_multi_line = False
        for i in range(0, len(text) ) :
            line = text[i]
            if in_multi_line :
                if line.strip() == "-----" :
                    if key=="COMMENT" :
                        comment = self.parse_comment(text[in_multi_line:i])
                        article.comments.append(comment)
                        #comment = self.parse_comment(text[in_multi_line:i])
                        #entry["COMMENT"].append(comment)
                    elif key=="BODY":
                        article.body = "".join(text[in_multi_line:i])
                    elif key=="EXTENDED BODY":
                        article.extended_body = "".join(text[in_multi_line:i])
                    in_multi_line = False
            else :
                tmp = line.split(":", 1)
                key = tmp[0]
                if key in single_line :
                    #delete the first space character
                    #value = tmp[1][1:]
                    value = tmp[1].strip()
                    if key == "TITLE" :
                        article.title = value
                    elif key == "AUTHOR" :
                        article.author = value
                    elif key == "DATE" :
                        article.date = parse_date(value)
                    elif key == "PRIMARY CATEGORY" or key == "CATEGORY" :
                        article.category.append(value)
                    elif key == "STATUS" :
                        if value=="draft" : self.status = Article.DRAFT
                elif key in multi_line :
                    in_multi_line = i+1

        #for k, v in entry.iteritems() :
            #print k,"*****"
            #print v
        #self.entries.append(entry)
        self.blogdata.articles.append(article)

    def parse(self) :
        f = codecs.open(self.filename, encoding="utf-8")
        lines = f.readlines()

        entries_text = self.split_array(lines, "--------")
        for text in entries_text :
            self.parse_entry(text)

        f.close()
        return self.blogdata


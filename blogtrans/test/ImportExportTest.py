import unittest

import os
import random

# Importers / Exporters
from blogtrans.wretch.WretchImporter import WretchImporter
from blogtrans.mt import *

from blogtrans.blogger.BloggerExporter import *
from blogtrans.blogger.BloggerImporter import *

def _get_file_fullname(format, filename) :
    return "TestData/%s/%s" % (format, filename)

class _ImportTask(object) :
    def __init__(self, format, filename) :
        self.format = format
        self.filename = filename

        self.importer_class = globals()["%sImporter" % format]

    def do_import(self) :
        file_fullname = _get_file_fullname(self.format, self.filename)
        importer = self.importer_class (file_fullname)
        self.blogdata = importer.parse()
        assert self.blogdata.article_count() > 0
        assert self.blogdata.comment_count() > 0

    def do_export_blogger(self) :
        exporter = BloggerExporter("testfile", self.blogdata)
        exporter.Export()

        #importer = BloggerImporter("testfile")
        #blogdata = importer.parse()
        #assert len(blogdata.articles) == len(self.blogdata.articles)
        #assert blogdata.comment_count() == self.blogdata.comment_count()

    def do_export_mt(self) :
        exporter = MTExporter("testfile", self.blogdata)
        exporter.Export()

        importer = MTImporter("testfile")
        blogdata = importer.parse()
        #print len(blogdata.articles) , len(self.blogdata.articles), blogdata.comment_count(), self.blogdata.comment_count()
        assert len(blogdata.articles) == len(self.blogdata.articles)
        assert blogdata.comment_count() == self.blogdata.comment_count()

def _make_filelist(format) :
    path = "TestData/%s/" % format
    filenames = os.listdir(path)
    return filenames

def _make_testcase_by_format(format) :
    filenames = _make_filelist("Wretch")

    testcases = []

    for filename in filenames :
        task = _ImportTask(format, filename)
        testcase = unittest.FunctionTestCase(task.do_import, description="Import %s : %s" % (format, filename) )
        testcases.append(testcase)

        testcase = unittest.FunctionTestCase(task.do_export_blogger, description="BloggerExporter%s : %s" % (format, filename) )
        testcases.append(testcase)

        testcase = unittest.FunctionTestCase(task.do_export_mt, description="MTExporter%s : %s" % (format, filename) )
        testcases.append(testcase)


    return testcases

def make_testcases() :
    return _make_testcase_by_format("Wretch")

# -*- coding: utf-8 -*-
# @Time    : 2018/4/27 15:15
# @Author  : XuWenzhong
# @Email   : xuwenzhong1994@163.com
# @File    : CrawlXpath.py
# @Version : 1.0.1
# @Software: PyCharm

import pymongo
from UniversalCrawl import settings
from UniversalCrawl.utils import *
from flask import jsonify
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class CrawlXpath(object):
    """docstring for CrawlXpath
    Some operations about CrawlXpath
    """

    def __init__(self, req):
        self.mongo_uri = settings.MONGO_URI
        self.mongo_db = settings.MONGO_DATABASE

        self.opertype = req.args['type'] if 'type' in req.args else None
        self.spider = "Universal"
        self.rulename = req.args['rulename'] if 'rulename' in req.args else None
        self.allow_domains = req.args['allow_domains'] if 'allow_domains' in req.args else None
        self.start_urls = req.args['start_urls'] if 'start_urls' in req.args else None
        # self.allow_url = req.args['allow_url'] if 'allow_url' in req.args else None
        # self.extract_from = req.args['extract_from'] if 'extract_from' in req.args else None
        self.title_gettype = req.args['titleGetType'] if 'titleGetType' in req.args else None
        self.title_xpath = req.args['title_xpath'] if 'title_xpath' in req.args else None
        self.srcurl_gettype = req.args['srcUrlGetType'] if 'srcUrlGetType' in req.args else None
        self.srcurl_xpath = req.args['srcUrl_xpath'] if 'srcUrl_xpath' in req.args else None
        self.src_gettype = req.args['srcGetType'] if 'srcGetType' in req.args else None
        self.src_xpath = req.args['src_xpath'] if 'src_xpath' in req.args else None
        self.src_re = req.args['src_re'] if 'src_re' in req.args else None
        self.datetime_gettype = req.args['datetimeGetType'] if 'datetimeGetType' in req.args else None
        self.datetime_xpath = req.args['datetime_xpath'] if 'datetime_xpath' in req.args else None
        self.datetime_re = req.args['datetime_re'] if 'datetime_re' in req.args else None
        self.author_gettype = req.args['authorGetType'] if 'authorGetType' in req.args else None
        self.author_xpath = req.args['author_xpath'] if 'author_xpath' in req.args else None
        self.author_re = req.args['author_re'] if 'author_re' in req.args else None
        self.content_gettype = req.args['contentGetType'] if 'contentGetType' in req.args else None
        self.content_xpath = req.args['content_xpath'] if 'content_xpath' in req.args else None
        self.orgsrc = req.args['orgsrc'] if 'orgsrc' in req.args else None
        self.sitename = req.args['siteName'] if 'siteName' in req.args else None
        self.type = req.args['summary'] if 'summary' in req.args else None
        self.isfilter = req.args['isFilter'] if 'isFilter' in req.args else "是"
        self.isenable = req.args['isEnable'] if 'isEnable' in req.args else "1"

    def savexpath(self):
        rulename = self.rulename
        document = {
            "spider": self.spider,
            "website": self.sitename,
            "type": self.type,
            "index": "http://tech.china.com/",
            # "start_urls": self.start_urls,
            "start_urls": {
                "type": "dynamic",
                "method": "china",
                "args": [
                    5,
                    10
                ]
            },
            "allowed_domains": self.allow_domains,
            "rulename": self.rulename,
            # "allow_url": self.allow_url,
            # "extract_from": self.extract_from,

            "isfilter": self.isfilter,
            "isenable": self.isenable,
            "item": {
                "class": "UniversalcrawlItem",
                "loader": "ChinaLoader",
                "attrs": {
                    "_id": [
                        {
                            "method": self.title_gettype,
                            "args": [
                                self.title_xpath
                            ]
                        }
                    ],
                    "title": [
                        {
                            "method": self.title_gettype,
                            "args": [
                                self.title_xpath
                            ]
                        }
                    ],
                    "srcUrl": [
                        {
                            "method": self.srcurl_gettype,
                            "args": [
                                self.srcurl_xpath
                            ]
                        }
                    ],
                    "content": [
                        {
                            "method": self.content_gettype,
                            "args": [
                                self.content_xpath
                            ]
                        }
                    ],
                    "datetime": [
                        {
                            "method": self.datetime_gettype,
                            "args": [
                                self.datetime_xpath
                            ],
                            "re": self.datetime_re
                        }
                    ],
                    "src": [
                        {
                            "method": self.src_gettype,
                            "args": [
                                self.src_xpath
                            ],
                            "re": self.src_re
                        }
                    ],
                    "siteName": [
                        {
                            "method": "value",
                            "args": [
                                self.sitename
                            ]
                        }
                    ]
                }
            }
        }
        try:
            set_config(rulename, document)
            return "ok"
        except Exception as e:
            raise e
        
    def removexpath(self):
        rulename = self.rulename
        try:
            remove_config(rulename)
        except Exception as e:
            raise e

    def getxpathinfo(self):
        name = self.rulename
        config = get_config(name)
        jsonres = jsonify(config)
        return jsonres
    
    def getxpathdbinfo(self, query={}):
        client = pymongo.MongoClient(self.mongo_uri)
        db = client[self.mongo_db]
        if len(query) == 0:
            query["isenable"] = "1"
        else:
            pass
        objlist = db.siteInfo_xpath.find(query).sort([("rulename", 1)])
        return objlist

    def operxpath(self):
        if self.opertype == "EditXPath":
            return self.savexpath()
        elif self.opertype == "removexpath":
            return self.removexpath()
        elif self.opertype == "GetXpath":
            return self.getxpathinfo()
        else:
            pass
    
    @staticmethod
    def returnsuccessmsg(info):
        data = {
            "state": "ok",
            "msg": info
        }
        jsonres = jsonify(data)
        return jsonres

    @staticmethod
    def returnerrmsg(info):
        data = {
            "state": "err",
            "msg": info
        }
        return jsonify(data)


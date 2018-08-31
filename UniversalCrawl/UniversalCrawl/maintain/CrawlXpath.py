# -*- coding: utf-8 -*-
# @Time    : 2018/4/27 15:15
# @Author  : XuWenzhong
# @Email   : xuwenzhong1994@163.com
# @File    : CrawlXpath.py
# @Version : 1.0.1
# @Software: PyCharm

import pymongo
from UniversalCrawl import settings
import csv
import codecs
from flask import jsonify
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class CrawlXpath(object):
    """docstring for CrawlXpath
    Some operations baout CrawlXpath
    """

    def __init__(self, req):
        self.mongo_uri = settings.MONGO_URI
        self.mongo_db = settings.MONGO_DATABASE

        self.opertype = req.args['type'] if 'type' in req.args else None
        self.rulename = req.args['objInfo[rulename]'] if 'objInfo[rulename]' in req.args else None
        self.allow_domains = req.args['objInfo[allow_domains]'] if 'objInfo[allow_domains]' in req.args else None
        self.start_urls = req.args['objInfo[start_urls]'] if 'objInfo[start_urls]' in req.args else None
        self.allow_url = req.args['objInfo[allow_url]'] if 'objInfo[allow_url]' in req.args else None
        self.extract_from = req.args['objInfo[extract_from]'] if 'objInfo[extract_from]' in req.args else None
        self.title_xpath = req.args['objInfo[title_xpath]'] if 'objInfo[title_xpath]' in req.args else None
        self.src_xpath = req.args['objInfo[src_xpath]'] if 'objInfo[src_xpath]' in req.args else None
        self.src_re = req.args['objInfo[src_re]'] if 'objInfo[src_re]' in req.args else None
        self.datetime_xpath = req.args['objInfo[datetime_xpath]'] if 'objInfo[datetime_xpath]' in req.args else None
        self.datetime_re = req.args['objInfo[datetime_re]'] if 'objInfo[datetime_re]' in req.args else None
        self.author_xpath = req.args['objInfo[author_xpath]'] if 'objInfo[author_xpath]' in req.args else None
        self.author_re = req.args['objInfo[author_re]'] if 'objInfo[author_re]' in req.args else None
        self.content_xpath = req.args['objInfo[content_xpath]'] if 'objInfo[content_xpath]' in req.args else None
        self.orgsrc = req.args['objInfo[orgsrc]'] if 'objInfo[orgsrc]' in req.args else None
        self.sitename = req.args['objInfo[siteName]'] if 'objInfo[siteName]' in req.args else None
        self.summary = req.args['objInfo[summary]'] if 'objInfo[summary]' in req.args else None
        self.isfilter = req.args['objInfo[isFilter]'] if 'objInfo[isFilter]' in req.args else "是"
        self.isenable = req.args['objInfo[isEnable]'] if 'objInfo[isEnable]' in req.args else "1"

    def savexpath(self):
        client = pymongo.MongoClient(self.mongo_uri)
        db = client[self.mongo_db]
        param = {
            "_id": self.rulename
        }
        document = {
            "_id": self.rulename,
            "rulename": self.rulename,
            "allowed_domains": self.allow_domains,
            "start_urls": self.start_urls,
            "allow_url": self.allow_url,
            "extract_from": self.extract_from,
            "title_xpath": self.title_xpath,
            "src_xpath": self.src_xpath,
            "src_re": self.src_re,
            "datetime_xpath": self.datetime_xpath,
            "datetime_re": self.datetime_re,
            "author_xpath": self.author_xpath,
            "author_re": self.author_re,
            "content_xpath": self.content_xpath,
            "orgsrc": self.orgsrc,
            "sitename": self.sitename,
            "isfilter": self.isfilter,
            "summary": self.summary,
            "isenable": self.isenable
        }
        try:
            info = db.siteInfo_xpath.update(param, {"$set": document}, upsert=True)
            return self.returnsuccessmsg(info) if len(info) > 0 else self.returnerrmsg(info)
        except Exception as e:
            raise e
        
    def removexpath(self):
        client = pymongo.MongoClient(self.mongo_uri)
        db = client[self.mongo_db]
        param = {
            "_id": self.rulename
        }
        try:
            info = db.siteInfo_xpath.remove(param)
            return self.returnsuccessmsg(info) if info['ok'] == 1.0 and info['n'] > 0 else self.returnerrmsg(info)
        except Exception as e:
            raise e
    
    def getxpathinfo(self):
        param = {
            "start_urls": self.start_urls,
            "orgsrc": self.orgsrc
        }
        datas = self.getxpathdbinfo(param)
        return jsonify(list(datas))
    
    def getxpathdbinfo(self, query={}):
        client = pymongo.MongoClient(self.mongo_uri)
        db = client[self.mongo_db]
        if len(query) == 0:
            query["isenable"] = "启用"
        else:
            pass
        objlist = db.siteInfo_xpath.find(query).sort([("rulename", 1)])
        return objlist
    
    def updatecsvfile(self):
        datas = self.getxpathdbinfo()
        with open('CreditCrawl/maintain/SiteInfo.csv', 'wb') as csvfileWriter:
            csvfileWriter.write(codecs.BOM_UTF8)
            writer = csv.writer(csvfileWriter)
            fieldlist = [
                "rulename",
                "allowed_domains",
                "start_urls",
                "allow_url",
                "extract_from",
                "title_xpath",
                "src_xpath",
                "src_re",
                "datetime_xpath",
                "datetime_re",
                "author_xpath",
                "author_re",
                "content_xpath",
                "orgsrc",
                "sitename",
                "isfilter",
                "summary",
                "isenable"
            ]
            writer.writerow(fieldlist)
            for data in datas:
                datavaluelst = []
                for field in fieldlist:
                    if field not in data:
                        datavaluelst.append("None")
                    else:
                        datavaluelst.append(data[field])
                try:
                    writer.writerow(datavaluelst)
                except Exception as e:
                    print "write csv exception. e = { %s }" % e
    
    def operxpath(self):
        if self.opertype == "EditXPath":
            return self.savexpath()
        elif self.opertype == "removexpath":
            return self.removexpath()
        elif self.opertype == "GetXpath":
            return self.getxpathinfo()
        else:
            pass
    
    def returnsuccessmsg(self, info):
        self.updatecsvfile()
        data = dict()
        data["state"] = "ok"
        data["msg"] = info
        jsonres = jsonify(data)
        return jsonres
    
    def returnerrmsg(self, info):
        self.updatecsvfile()
        data = dict()
        data["state"] = "err"
        data["msg"] = info
        return jsonify(data)

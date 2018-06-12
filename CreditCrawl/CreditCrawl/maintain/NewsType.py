# -*- coding: utf-8 -*-
# @Time    : 2018/4/27 15:28
# @Author  : XuWenzhong
# @Email   : xuwenzhong1994@163.com
# @File    : NewsType.py
# @Version : 1.0.1
# @Software: PyCharm

import pymongo
from CreditCrawl import settings
from flask import jsonify
import json


class NewsType(object):
    """
    docstring for NewsType
    Some operations about newstype
    """

    def __init__(self, pbotype, pbotypename, opertype):
        self.mongo_uri = settings.MONGO_URI
        self.mongo_db = settings.MONGO_DATABASE
        self.pbotype = pbotype
        self.pbotypename = pbotypename
        self.opertype = opertype

    def addnewstype(self):
        client = pymongo.MongoClient(self.mongo_uri)
        db = client[self.mongo_db]
        try:
            info = db.info_newstype.insert({"pbotype": self.pbotype, "pbotypename": self.pbotypename})
            return self.returnsuccessmsg() if len(info) > 0 else self.returnerrmsg(info)
        except Exception as e:
            raise e

    def deletenewstype(self):
        client = pymongo.MongoClient(self.mongo_uri)
        db = client[self.mongo_db]
        try:
            info = db.info_newstype.remove({"pbotype": self.pbotype})
            return self.returnsuccessmsg() if info['ok'] == 1.0 and info['n'] > 0 else self.returnerrmsg(info)
        except Exception as e:
            raise e

    def updatenewstype(self):
        client = pymongo.MongoClient(self.mongo_uri)
        db = client[self.mongo_db]
        document = {"pbotypename": self.pbotypename}
        try:
            info = db.info_newstype.update({"pbotype": self.pbotype}, {"$set": document})
            return self.returnsuccessmsg() if info['updatedExisting'] is True and info['ok'] == 1.0 and info[
                'n'] > 0 else self.returnerrmsg(info)
        except Exception as e:
            raise e

    def getnewstype(self):
        client = pymongo.MongoClient(self.mongo_uri)
        db = client[self.mongo_db]
        return db.info_newstype.find().sort([("pbotype", 1)])

    def updatetypefile(self):
        sobjinfos = list()
        datas = list(self.getnewstype())
        for data in datas:
            doc = dict(data)
            sobjinfo = dict()
            sobjinfo["pbotype"] = doc["pbotype"]
            sobjinfo["pbotypename"] = doc["pbotypename"]
            sobjinfos.append(sobjinfo)
        scontent = "var typeInfo_config= %s " % json.dumps(sobjinfos, ensure_ascii=False)
        with open('../static/javascripts/model/typeInfo_config.js', 'w') as f:
            f.write(scontent)

    def returnsuccessmsg(self):
        self.updatetypefile()
        data = dict()
        data["state"] = "ok"
        data["msg"] = "1"
        jsonres = jsonify(data)
        return jsonres

    def returnerrmsg(self, info):
        self.updatetypefile()
        data = dict()
        data["state"] = "err"
        data["msg"] = info
        return jsonify(data)

    def opernewstype(self):
        if self.opertype == 'add':
            return self.addnewstype()
        elif self.opertype == 'edit':
            return self.updatenewstype()
        elif self.opertype == 'delete':
            return self.deletenewstype()
        else:
            pass

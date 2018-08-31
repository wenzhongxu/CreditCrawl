# -*- coding: utf-8 -*-
# @Time    : 2018/4/27 15:37
# @Author  : XuWenzhong
# @Email   : xuwenzhong1994@163.com
# @File    : SiteInfoCateConfig.py
# @Version : 1.0.1
# @Software: PyCharm

import pymongo
from UniversalCrawl import settings
from flask import jsonify


class SiteInfoCateconfig(object):
    """
    docstring for SiteInfoCateconfig
    the siteinfo about config
    """

    def __init__(self, req):
        self.mongo_uri = settings.MONGO_URI
        self.mongo_db = settings.MONGO_DATABASE

        self.sReqType = req.args['type'] if 'type' in req.args else None
        if 'objInfo[_id]' in req.args:
            self._id = req.args['objInfo[_id]']
        elif 'nodeObj[_id]' in req.args:
            self._id = req.args['nodeObj[_id]']
        else:
            self._id = ''

        self.src = req.args['objInfo[src]'] if 'objInfo[src]' in req.args else None

        self.remark = req.args['objInfo[remark]'] if 'objInfo[remark]' in req.args else None

        self.Summary = req.args['objInfo[Summary]'] if 'objInfo[Summary]' in req.args else None

        if 'objInfo[site]' in req.args:
            self.site = req.args['objInfo[site]']
        elif 'nodeObj[site]' in req.args:
            self.site = req.args['nodeObj[site]']
        else:
            self.site = ''

        self.siteName = req.args['objInfo[siteName]'] if 'objInfo[siteName]' in req.args else None

        self.IsFilter = req.args['objInfo[IsFilter]'] if 'objInfo[IsFilter]' in req.args else None

        self.isEnable = req.args['objInfo[isEnable]'] if 'objInfo[isEnable]' in req.args else "1"

        self.pId = req.args['nodeObj[pId]'] if 'nodeObj[pId]' in req.args else None

        self.name = req.args['nodeObj[name]'] if 'nodeObj[name]' in req.args else None

        self.isParent = req.args['nodeObj[isParent]'] if 'nodeObj[isParent]' in req.args else None

    def getcate(self, req):
        collection = "siteInfo_cateConfig"
        return self.getdata4db(req, collection)

    def savecate(self):
        client = pymongo.MongoClient(self.mongo_uri)
        db = client[self.mongo_db]
        param = {
            "_id": self._id
        }
        document = {
            "_id": self._id,
            "pId": self.pId,
            "name": self.name,
            "site": self.site,
            "isParent": self.isParent
        }
        try:
            info = db.siteInfo_cateConfig.update(param, {"$set": document}, upsert=True)
            return self.returnsuccessmsg(document) if len(info) > 0 else self.returnerrmsg(info)
        except Exception as e:
            raise e

    def removecate(self):
        client = pymongo.MongoClient(self.mongo_uri)
        db = client[self.mongo_db]
        param = {
            "_id": self._id
        }
        document = {
            "_id": self._id,
            "pId": self.pId,
            "name": self.name,
            "site": self.site,
            "isParent": self.isParent
        }
        try:
            info = db.siteInfo_cateConfig.remove(param)
            return self.returnsuccessmsg(document) if info['ok'] == 1.0 and info['n'] > 0 else self.returnerrmsg(info)
        except Exception as e:
            raise e

    def getsite(self, req):
        collection = "siteInfo_config"
        return self.getdata4db(req, collection, 1)

    def savesite(self):
        client = pymongo.MongoClient(self.mongo_uri)
        db = client[self.mongo_db]
        param = {
            "_id": self._id
        }
        document = {
            "_id": self._id,
            "src": self.src,
            "remark": self.remark,
            "Summary": self.Summary,
            "site": self.site,
            "siteName": self.siteName,
            "IsFilter": self.IsFilter,
            "isEnable": self.isEnable
        }
        try:
            info = db.siteInfo_config.update(param, {"$set": document}, upsert=True)
            return self.returnsuccessmsg(document) if info['ok'] == 1.0 and info['n'] > 0 else self.returnerrmsg(info)
        except Exception as e:
            raise e

    def removesite(self):
        client = pymongo.MongoClient(self.mongo_uri)
        db = client[self.mongo_db]
        param = {
            "_id": self._id
        }
        paramxpath = {
            "_id": self._id,
            "siteName": self.siteName
        }
        document = {
            "_id": self._id,
            "src": self.src,
            "remark": self.remark,
            "Summary": self.Summary,
            "site": self.site,
            "siteName": self.siteName,
            "IsFilter": self.IsFilter,
            "isEnable": self.isEnable
        }
        try:
            info = db.siteInfo_config.remove(param)
            db.siteInfo_xpath.remove(paramxpath)
            return self.returnsuccessmsg(document) if info['ok'] == 1.0 and info['n'] > 0 else self.returnerrmsg(info)
        except Exception as e:
            raise e

    '''
    从数据库获取数据信息
    :isSite : 是否是站点信息
    :return : queryResult
    '''

    def getdata4db(self, req, col, issite=None):
        client = pymongo.MongoClient(self.mongo_uri)
        db = client[self.mongo_db]
        query = {}
        if issite is not None:
            if not req.args['site'] is None:
                query["site"] = req.args['site']
            elif not req.args['_id'] is None:
                scond = req.args['_id']
                if scond.indexOf('/') > 0:
                    # scond = scond.replace(/\//g,'\\/')
                    # scond='/^.*?'+scond+'.*$/'
                    pass
                else:
                    # sCond='/^.*?\\/'+sCond+'\\/.*$/'
                    pass
                eval("query={_id:%s}" % scond)
        else:
            pass
        objlist = db[col].find(query)
        return self.returnsuccessmsg(list(objlist))

    @staticmethod
    def returnsuccessmsg(nodeobj):
        data = dict()
        data["state"] = "ok"
        data["objList"] = nodeobj
        jsonres = jsonify(data)
        return jsonres

    @staticmethod
    def returnerrmsg(info):
        data = dict()
        data["state"] = "err"
        data["msg"] = info
        return jsonify(data)

    def opersiteconfig(self, req):
        if self.sReqType is not None:
            if self.sReqType == "site":
                return self.getsite(req)
            elif self.sReqType == "saveSite":
                return self.savesite()
            elif self.sReqType == "removeSite":
                return self.removesite()
            elif self.sReqType == "cate":
                return self.getcate(req)
            elif self.sReqType == "saveCate":
                return self.savecate()
            elif self.sReqType == "removeCate":
                return self.removecate()
            else:
                pass
        else:
            pass

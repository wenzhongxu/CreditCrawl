# -*- coding: utf-8 -*-
# @Time    : 2018/4/27 14:52
# @Author  : XuWenzhong
# @Email   : xuwenzhong1994@163.com
# @File    : SearchApi.py
# @Version : 1.0.1
# @Software: PyCharm

import pymongo
import sys
import settings
from flask import jsonify

sys.path.append("..")

'''
    搜索接口:http://localhost:5000/search?begdate=2017-08-09&type=list
'''


def search(req):
    client = pymongo.MongoClient(settings.MONGO_URI)
    db = client[settings.MONGO_DATABASE]
    collectionname = "info_detail"
    queryparams = {}
    skip = 0
    limit = 500

    if 'type' in req.args and req.args['type'] == 'email':
        collectionname = "info_detail4email"
    else:
        pass

    if 'title' in req.args and req.args['title'] != '':
        queryparams['_id'] = req.args['title']
    else:
        pass

    if 'author' in req.args and req.args['author'] != '':
        queryparams["author"] = req.args['author']
    else:
        pass

    if 'src' in req.args and req.args['src'] != '':
        queryparams["src"] = req.args['src']
    else:
        pass

    if 'url' in req.args and req.args['url'] != '':
        queryparams["srcUrl"] = req.args['url']
    else:
        pass

    if 'begdate' in req.args and req.args['begdate'] != '' and 'enddate' in req.args and req.args['enddate'] != '':
        queryparams["updatetime"] = {"$gt": req.args['begdate'], "$lte": req.args['enddate']}
    elif 'begdate' in req.args and req.args['begdate'] != '':
        queryparams["updatetime"] = {"$gt": req.args['begdate']}
    elif 'enddate' in req.args and req.args['enddate'] != '':
        queryparams["updatetime"] = {"$lte": req.args['enddate']}
    else:
        pass

    if 'pagenum' in req.args and req.args['pagenum'] != '' and 'page' in req.args and req.args['page'] != '':
        pagenum = int(req.args['pagenum'])
        page = int(req.args['page'])
        skip = pagenum * (page - 1)
        limit = pagenum
    else:
        pass
    results = db[collectionname].find(queryparams).sort([('updatetime', -1)]).skip(skip).limit(limit)
    return jsonify(list(results))


def getsite():
    client = pymongo.MongoClient(settings.MONGO_URI)
    db = client[settings.MONGO_DATABASE]
    collectionname = "siteInfo_config"
    queryparams = {}
    queryparams['isEnable'] = "1"
    results = db[collectionname].find(queryparams, {"_id": 0, "ruleName": 1})
    return list(results)



# -*- coding: utf-8 -*-
# @Time    : 2018/8/13 19:13
# @Author  : XuWenzhong
# @Email   : xuwenzhong1994@163.com
# @File    : run.py
# @Version : 1.0.1
# @Software: PyCharm

import sys
from scrapy.utils.project import get_project_settings
from utils import get_config
from scrapy.crawler import CrawlerProcess
import pymongo
import settings
sys.path.append("../")


def run():
    if len(sys.argv) > 1:
        crawlsites = [sys.argv[1]]
    else:
        crawlsites = getsite()
    for crawlsite in crawlsites:
        name = crawlsite["ruleName"]
        custom_settings = get_config(name)
        if custom_settings == "" or name is None:
            continue
        spider = custom_settings.get('spider', 'Universal')
        project_settings = get_project_settings()
        settings = dict(project_settings.copy())
        settings.update(custom_settings.get('settings'))
        process = CrawlerProcess(settings)
        process.crawl(spider, **{'name': name})
        process.start()


def getsite():
    client = pymongo.MongoClient(settings.MONGO_URI)
    db = client[settings.MONGO_DATABASE]
    collectionname = "siteInfo_config"
    queryparams = {}
    queryparams['isEnable'] = "1"
    results = db[collectionname].find(queryparams, {"_id": 0, "ruleName": 1})
    return list(results)


if __name__ == '__main__':
    run()


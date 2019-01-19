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
import time
from scrapy.utils.log import configure_logging
from conf.config import log_format, log_file, log_path, log_open
import datetime
import os
import logging
sys.path.append("../")


def run():
    print "CreditcrawlSpider is started in ", time.strftime("%Y-%m-%d %H:%M:%S")
    spider_settings = config_setttings()
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
        spider_settings.update(custom_settings.get('settings'))
        process = CrawlerProcess(spider_settings)
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


def config_setttings():
    # 配置日志记录规则设置
    configure_logging(install_root_handler=False)
    project_settings = get_project_settings()
    # 初始化日志路径
    if log_open is True:
        project_settings.set("LOG_LEVEL", 'INFO')
        logpath = datetime.datetime.now().strftime(log_path)
        if not os.path.isdir(logpath):
            os.makedirs(logpath)
        logging.basicConfig(
            filename=datetime.datetime.now().strftime('%s/%s_spider.log' % (logpath, log_file)),
            format=log_format,
            level=logging.INFO
        )
    return dict(project_settings.copy())


if __name__ == '__main__':
    run()


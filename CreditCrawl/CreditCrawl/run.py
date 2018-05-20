# -*- coding: utf-8 -*-
# @Time    : 2018/4/27 14:46
# @Author  : XuWenzhong
# @Email   : xuwenzhong1994@163.com
# @File    : run.py
# @Version : 1.0.1
# @Software: PyCharm

import csv
import codecs
import os
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings
from scrapy.utils.log import configure_logging
from spiders.creditCrawl import CreditcrawlSpider
import time
import datetime
import logging
from conf.config import runsleep
from conf.config import log_format, log_file, log_path, log_open
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def startcrawl():
    print "CreditcrawlSpider is started in ", time.strftime("%Y-%m-%d %H:%M:%S")
    reactor.callLater(runsleep, startcrawl)
    settings = get_project_settings()

    # 配置日志记录规则设置
    configure_logging(install_root_handler=False)
    # configure_logging()
    # 初始化日志路径
    if log_open is True:
        settings.set("LOG_LEVEL", 'INFO')
        logpath = datetime.datetime.now().strftime(log_path)
        if not os.path.isdir(logpath):
            os.makedirs(logpath)
        logging.basicConfig(
            filename=datetime.datetime.now().strftime('%s/%s_spider.log' % (logpath, log_file)),
            format=log_format,
            level=logging.INFO
        )
    runner = CrawlerRunner(settings)
    with codecs.open("maintain/SiteInfo.csv", 'rU', 'utf-8-sig') as f:
        rules = csv.DictReader(f)
        for rule in rules:
            print(rule['sitename'])
            runner.crawl(CreditcrawlSpider, rule=rule)


if __name__ == '__main__':
    startcrawl()
    reactor.run()


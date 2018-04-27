# -*- coding: utf-8 -*-
# @Time    : 2018/4/27 14:46
# @Author  : XuWenzhong
# @Email   : xuwenzhong1994@163.com
# @File    : run.py
# @Version : 1.0.1
# @Software: PyCharm

import csv
import codecs
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from spiders.creditCrawl import CreditcrawlSpider
import time
from conf.config import runsleep


def startcrawl():
    print "CreditcrawlSpider is started in ", time.strftime("%Y-%m-%d %H:%M:%S")
    reactor.callLater(runsleep, startcrawl)
    settings = get_project_settings()
    configure_logging(settings)
    runner = CrawlerRunner(settings)
    with codecs.open("SiteInfo.csv", 'rU', 'utf-8-sig') as f:
        rules = csv.DictReader(f)
        for rule in rules:
            print(rule['sitename'])
            runner.crawl(CreditcrawlSpider, rule=rule)


if __name__ == '__main__':
    startcrawl()
    reactor.run()


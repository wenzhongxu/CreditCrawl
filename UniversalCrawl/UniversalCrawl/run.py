# -*- coding: utf-8 -*-
# @Time    : 2018/8/13 19:13
# @Author  : XuWenzhong
# @Email   : xuwenzhong1994@163.com
# @File    : run.py
# @Version : 1.0.1
# @Software: PyCharm

import sys
import os
import os.path
from scrapy.utils.project import get_project_settings
# from UniversalCrawl.spiders.Universal import UniversalSpider
from utils import get_config
from scrapy.crawler import CrawlerProcess


def run():
    if len(sys.argv) > 1:
        names = [sys.argv[1]]
    else:
        crawlsites = getsite()
        names = crawlsites
    for name in names:
        custom_settings = get_config(name)
        spider = custom_settings.get('spider', 'Universal')
        project_settings = get_project_settings()
        settings = dict(project_settings.copy())
        settings.update(custom_settings.get('settings'))
        process = CrawlerProcess(settings)
        process.crawl(spider, **{'name': name})
        process.start()


def getsite():
    rootdir = "./configs"  # 指明被遍历的文件夹
    sites = []
    # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    for parent, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:  # 输出文件信息
            index = filename.rfind('.')
            name = filename[:index]
            sites.append(name)
    return sites


if __name__ == '__main__':
    run()


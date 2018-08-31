# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UniversalcrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 标题
    _id = scrapy.Field()
    title = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 发布时间
    datetime = scrapy.Field()
    # 来源网站
    src = scrapy.Field()
    # 新闻内容
    content = scrapy.Field()
    # 新闻类别(guid)
    summary = scrapy.Field()
    # 频道
    orgSrc = scrapy.Field()
    # 站点名称
    siteName = scrapy.Field()
    # 新闻原网址
    srcUrl = scrapy.Field()
    # 抓取时间
    updatetime = scrapy.Field()
    # 是否过滤负面关键字
    isfilter = scrapy.Field()

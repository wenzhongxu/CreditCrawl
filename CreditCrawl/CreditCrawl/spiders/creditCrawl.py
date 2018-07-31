# -*- coding: utf-8 -*-
# @Time    : 2018/4/27 10:45
# @Author  : XuWenzhong
# @Email   : xuwenzhong1994@163.com
# @File    : creditCrawl.py
# @Version : 1.0.1
# @Software: PyCharm


from items import CreditcrawlItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
from datetime import datetime
from tools import formatdate
from tools import myUtil


class CreditcrawlSpider(CrawlSpider):
    name = 'CreditCrawl'

    def __init__(self, rule):
        self.rule = rule
        self.name = rule["rulename"]
        self.allowed_domains = rule["allowed_domains"].split(",")
        self.start_urls = rule["start_urls"].split(",")

        rule_list = list()
        # 添加'下一页'的规则
        # if rule["NEXT_PAGE"]:
        #     rule_list.append(Rule(LinkExtractor(restrict_xpaths = rule["NEXT_PAGE"])))
        # 添加抽取文章链接的规则
        rule_list.append(Rule(LinkExtractor(
            allow=re.compile(eval(rule["allow_url"])),
            restrict_xpaths=rule["extract_from"]),
            callback='parse_item',
            follow=False))
        self.rules = tuple(rule_list)

        super(CreditcrawlSpider, self).__init__()

    def parse_item(self, response):
        self.log('This is a news page! %s' % response.url)

        newsitem = CreditcrawlItem()

        # 标题
        title = response.xpath(self.rule["title_xpath"]).extract_first()
        newsitem["_id"] = title
        newsitem["title"] = title

        # 发布时间
        if self.rule["datetime_re"]:
            pubtime = response.xpath(self.rule["datetime_xpath"]).re_first(self.rule["datetime_re"])
        else:
            pubtime = response.xpath(self.rule["datetime_xpath"]).extract_first()
        # 发布时间处理成统一格式
        pubtime = formatdate.DateFormatHelper().convertstandarddateformat(pubtime)
        newsitem["datetime"] = pubtime

        # 链接
        newsitem["srcUrl"] = response.url

        # 作者
        if self.rule["author_re"]:
            author = response.xpath(self.rule["author_xpath"]).re_first(self.rule["author_re"])
        else:
            author = response.xpath(self.rule["author_xpath"]).extract_first()
        newsitem["author"] = author

        # 内容
        content_temp = "".join([tt.strip() for tt in response.xpath(self.rule["content_xpath"]).extract()])
        re_con_strong = re.compile(r'</strong>(\s*)<strong>')
        content_temp = re_con_strong.sub(r'\1', content_temp)
        re_start_strong = re.compile(r'<strong>', re.I)
        content_temp = re_start_strong.sub('<p>', content_temp)
        re_end_strong = re.compile(r'</strong>', re.I)
        content_temp = re_end_strong.sub('</p>', content_temp)
        newsitem['content'] = myUtil.filter_tags(content_temp)

        # 频道
        newsitem["orgSrc"] = self.rule["orgsrc"].encode("utf8")
        # 网站名称
        newsitem["siteName"] = self.rule["sitename"].encode("utf8")
        # 来源——抓取所得
        if self.rule["src_re"]:
            src = response.xpath(self.rule["src_xpath"]).re_first(self.rule["src_re"])
        else:
            src = response.xpath(self.rule["src_xpath"]).extract_first()
        newsitem["src"] = src
        # 分类
        newsitem["summary"] = self.rule["summary"]
        # 更新时间
        newsitem["updatetime"] = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S.%f')
        # 是否过滤负面关键字
        newsitem["isfilter"] = self.rule["isfilter"].encode("utf8")

        yield newsitem

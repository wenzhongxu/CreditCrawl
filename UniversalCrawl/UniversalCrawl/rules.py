# -*- coding: utf-8 -*-
# @Time    : 2018/8/30 20:10
# @Author  : XuWenzhong
# @Email   : xuwenzhong1994@163.com
# @File    : rules.py
# @Version : 1.0.1
# @Software: PyCharm

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

rules = {
    'china': (
        Rule(LinkExtractor(allow='article\/.*\.html', restrict_xpaths='//div[@id="left_side"]//div[@class="con_item"]'),
             callback='parse_item'),
        Rule(LinkExtractor(restrict_xpaths='//div[@id="pageStyle"]//a[contains(., "下一页")]'))
    )
}

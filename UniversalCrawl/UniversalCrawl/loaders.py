# -*- coding: utf-8 -*-
# @Time    : 2018/4/27 15:13
# @Author  : XuWenzhong
# @Email   : xuwenzhong1994@163.com
# @File    : web.py
# @Version : 1.0.1
# @Software: PyCharm

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join, Compose


class NewsLoader(ItemLoader):
    default_output_processor = TakeFirst()


class ChinaLoader(NewsLoader):
    text_out = Compose(Join(), lambda s: s.strip())
    source_out = Compose(Join(), lambda s: s.strip())
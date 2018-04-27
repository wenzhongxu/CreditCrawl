# -*- coding: utf-8 -*-
# @Time    : 2018/4/27 10:34
# @Author  : XuWenzhong
# @Email   : xuwenzhong1994@163.com
# @File    : RandomProxy.py
# @Version : 1.0.1
# @Software: PyCharm

import random

'''
这个类主要用于产生随机代理
'''


class RandomProxy(object):

    def __init__(self, iplist):  # 初始化一下数据库连接
        self.iplist = iplist

    @classmethod
    def from_crawler(cls, crawler):
        # 从Settings中加载IPLIST的值
        return cls(crawler.settings.getlist('IPLIST'))

    '''
        在请求上添加代理
        :param request:
        :param spider:
        :return:
    '''
    def process_request(self, request, spider):
        proxy = random.choice(self.iplist)
        request.meta['proxy'] = proxy

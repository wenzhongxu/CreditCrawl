# -*- coding: utf-8 -*-
# @Time    : 2018/8/30 20:09
# @Author  : XuWenzhong
# @Email   : xuwenzhong1994@163.com
# @File    : urls.py
# @Version : 1.0.1
# @Software: PyCharm


def china(start, end):
    for page in range(start, end + 1):
        yield 'http://tech.china.com/articles/index_' + str(page) + '.html'

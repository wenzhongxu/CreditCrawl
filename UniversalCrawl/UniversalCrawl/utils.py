# -*- coding: utf-8 -*-
# @Time    : 2018/8/12 19:24
# @Author  : XuWenzhong
# @Email   : xuwenzhong1994@163.com
# @File    : utils.py
# @Version : 1.0.1
# @Software: PyCharm

from os.path import realpath, dirname
import json


def get_config(name):
    path = dirname(realpath(__file__)) + '/configs/' + name + '.json'
    with open(path, 'r') as f:
        return json.loads(f.read())

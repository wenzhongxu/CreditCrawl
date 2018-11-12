# -*- coding: utf-8 -*-
# @Time    : 2018/8/12 19:24
# @Author  : XuWenzhong
# @Email   : xuwenzhong1994@163.com
# @File    : utils.py
# @Version : 1.0.1
# @Software: PyCharm

from os.path import realpath, dirname
import json
import os


def get_config(name):
    if isinstance(name, unicode):
        path = dirname(realpath(__file__)) + '/configs/' + name + '.json'
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.loads(f.read())
        else:
            return ""
    else:
        return ""


def set_config(name, config_dict):
    path = dirname(realpath(__file__)) + '/configs/' + name + '.json'
    with open(path, "w+") as f:
        json.dump(config_dict, f)


def remove_config(name):
    path = dirname(realpath(__file__)) + '/configs/' + name + '.json'
    if os.path.exists(path):
        os.remove(path)


if __name__ == '__main__':
    aa = get_config("zhanzhangzhijia")
    print aa

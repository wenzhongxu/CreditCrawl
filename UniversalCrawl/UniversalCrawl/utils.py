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


def edit_config(name, key, value):
    path = dirname(realpath(__file__)) + '/configs/' + name + '.json'
    key_ = key.split(".")
    key_length = len(key_)
    with open(path, 'rb') as f:
        json_data = json.load(f)
        i = 0
        a = json_data
        while i < key_length:
            if i + 1 == key_length:
                a[key_[i]] = value
                i = i + 1
            else:
                a = a[key_[i]]
                i = i + 1
    f.close()
    with open(path, 'w') as f:
        json.dump(json_data, f)
    f.close()


def edit_filter_config(name, value):
    path = dirname(realpath(__file__)) + '/configs/' + name + '.json'
    with open(path, 'rb') as f:
        json_data = json.load(f)
        a = json_data
        a["item"]["attrs"]["isfilter"][0]["args"] = value
    f.close()
    with open(path, 'w') as f:
        json.dump(json_data, f)
    f.close()


if __name__ == '__main__':
    edit_filter_config("zhanzhangzhijia", "否")

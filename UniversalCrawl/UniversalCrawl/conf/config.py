# -*- coding: utf-8 -*-
# @Time    : 2019/1/19 15:31
# @Author  : XuWenzhong
# @Email   : xuwenzhong1994@163.com
# @File    : config.py
# @Version : 1.0.1
# @Software: PyCharm

# 执行周期  单位：秒
runsleep = 120

# 是否开启日志记录
log_open = True
# 日志文件的保存路径 支持绝对路径 时间参数自动解析
log_path = '../UniversalCrawl/log/%Y_%m_%d'
# 日志文件保存格式
log_file = '%H'
# 日志记录存储格式
log_format = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"

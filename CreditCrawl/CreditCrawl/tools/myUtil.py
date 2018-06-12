# -*- coding: utf-8 -*-
# @Time    : 2018/4/27 11:21
# @Author  : XuWenzhong
# @Email   : xuwenzhong1994@163.com
# @File    : myUtil.py
# @Version : 1.0.1
# @Software: PyCharm

import re
import sys
import smtplib
from contextlib import contextmanager
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os.path
import datetime
from bs4 import BeautifulSoup
from urlparse import urljoin

type = sys.getfilesystemencoding()
# from settings import IMAGES_STORE

"""
Topic: 一些工具类
Desc : 
"""


def filter_tags(htmlstr):
    """更深层次的过滤，类似instapaper或者readitlater这种服务，很有意思的研究课题
    过滤HTML中的标签
    将HTML中标签等信息去掉
    @param htmlstr HTML字符串.
    """
    # 先过滤CDATA
    re_pp = re.compile('</p>', re.I)  # 段落结尾
    re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
    re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
    re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
    re_br = re.compile('<br\s*?/?>')  # 处理换行
    re_h = re.compile('</?\w+[^>]*>')  # HTML标签
    re_comment = re.compile('<!--[^>]*-->')  # HTML注释

    s = re_pp.sub('\n', htmlstr)  # 段落结尾变换行符
    s = re_cdata.sub('', s)  # 去掉CDATA
    s = re_script.sub('', s)  # 去掉SCRIPT
    s = re_style.sub('', s)  # 去掉style
    s = re_br.sub('\n', s)  # 将br转换为换行
    s = re_h.sub('', s)  # 去掉HTML 标签
    s = re_comment.sub('', s)  # 去掉HTML注释
    # 去掉多余的空行
    blank_line = re.compile('\n+')
    s = blank_line.sub('\n', s)
    s = replace_charentity(s)  # 替换实体
    return "".join([t.strip() + '\n' for t in s.split('\n') if t.strip() != ''])


def replace_charentity(htmlstr):
    """
    ##替换常用HTML字符实体.
    #使用正常的字符替换HTML中特殊的字符实体.
    #你可以添加新的实体字符到CHAR_ENTITIES中,处理更多HTML字符实体.
    #@param htmlstr HTML字符串.
    """
    char_entities = {'nbsp': ' ', '160': ' ',
                     'lt': '<', '60': '<',
                     'gt': '>', '62': '>',
                     'amp': '&', '38': '&',
                     'quot': '"', '34': '"', }

    re_charentity = re.compile(r'&#?(?P<name>\w+);')
    sz = re_charentity.search(htmlstr)
    while sz:
        entity = sz.group()  # entity全称，如&gt;
        key = sz.group('name')  # 去除&;后entity,如&gt;为gt
        try:
            htmlstr = re_charentity.sub(char_entities[key], htmlstr, 1)
            sz = re_charentity.search(htmlstr)
        except KeyError:
            # 以空串代替
            htmlstr = re_charentity.sub('', htmlstr, 1)
            sz = re_charentity.search(htmlstr)
    return htmlstr


pat1 = re.compile(r'<div class="hzh_botleft">(?:.|\n)*?</div>')
pat2 = re.compile(r'<script (?:.|\n)*?</script>')
pat3 = re.compile(r'<a href="javascript:"(?:.|\n)*?</a>')


def clean_html(p_str):
    """html标签清理"""
    p_str = pat1.sub('', p_str)
    p_str = pat2.sub('', p_str)
    p_str = pat3.sub('', p_str)
    return '\n'.join(s for s in p_str.split('\n') if len(s.strip()) != 0)


def repalce(s, re_exp, repl_string):
    return re_exp.sub(repl_string, s)


def ltos(lst):
    """列表取第一个值"""
    if lst is not None and isinstance(lst, list):
        if len(lst) > 0:
            return lst[0].strip()
    return ''


@contextmanager
def session_scope(Session):
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def parse_text(extract_texts, rule_name, attr_name):
    """xpath的提取方式
    @param extract_texts: 被处理的文本数组
    @param rule_name: 规则名称
    @param attr_name: 属性名
    """
    custom_func = "%s_%s" % (rule_name, attr_name)
    if custom_func in globals():
        return globals()[custom_func](extract_texts)
    return '\n'.join(extract_texts).strip() if extract_texts else ""


pat4 = re.compile(r'\d{4}年\d{2}月\d{2}日')


def osc_publish_time(extract_texts):
    """发布时间的提取方式
    @param extract_texts: 被处理的文本数组
    """
    if extract_texts:
        single_text = ''.join(extract_texts).strip()
        res = re.search(pat4, single_text)
        return res.group() if res else ""
    return ""


def tx(xpath_obj):
    return ''.join(xpath_obj.extract()).strip()

    '''
    更新 img 图片链接信息
    @param domcontent: 被处理的文本内容
    @param host: 网站的路由
    '''


def updateimgsrc(domcontent, host):
    soup = BeautifulSoup(domcontent, "lxml")
    imglist = soup.find_all('img')
    for src in imglist:
        src['src'] = urljoin(host, src)
    return domcontent.html()


def iscontainkeywords(title):
    result = False
    with open("tools/keywords.txt", "r") as f:
        for line in f.read().splitlines():
            if line in title:
                result = True
                break
            else:
                result = False
        return result

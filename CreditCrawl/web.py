# -*- coding: utf-8 -*-
# @Time    : 2018/4/27 15:13
# @Author  : XuWenzhong
# @Email   : xuwenzhong1994@163.com
# @File    : web.py
# @Version : 1.0.1
# @Software: PyCharm

from flask import Flask
from flask import render_template
from flask import request
from CreditCrawl.search import SearchApi
from CreditCrawl.maintain import NewsType
from CreditCrawl.maintain import SiteInfoCateConfig
from CreditCrawl.maintain import CrawlXpath
import logging

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    results = None
    return render_template('index.html', results=results)


@app.route('/grapConfig')
def grapconfig():
    return render_template('grapConfig.html')


@app.route('/search')
@app.route('/search/')
def do_search():
    # http://localhost:5000/search?begdate=2017-08-09&type=add
    if request.args:
        results = SearchApi.search(request)
        return results
    else:
        pass


@app.route('/newstype')
def opernewstype():
    # http://{0}/newstype?pbotype={1}&pbotypename={2}&opertype={3}&_={4}
    if request.args:
        pbotype = request.args['pbotype'] if request.args['pbotype'] else None
        pbotypename = request.args['pbotypename'] if request.args['pbotypename'] else None
        opertype = request.args['opertype'] if request.args['opertype'] else None
        doc = NewsType.NewsType(pbotype, pbotypename, opertype)
        return doc.opertype()
    else:
        pass


@app.route('/config')
def config():
    if request.args:
        siteobj = SiteInfoCateConfig.SiteInfoCateconfig(request)
        results = siteobj.opersiteconfig(request)
        return results
    else:
        pass


@app.route('/save', methods=['POST'])
def saveconfig():
    pass


@app.route('/editxpath')
def editxpath():
    if request.args:
        xpathobj = CrawlXpath.CrawlXpath(request)
        results = xpathobj.operxpath()
        return results
    else:
        pass


if __name__ == '__main__':
    handler = logging.FileHandler('flask2.log', encoding='UTF-8')
    handler.setLevel(logging.DEBUG)
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')

    handler.setFormatter(logging_format)

    app.logger.addHandler(handler)
    app.run(debug=True)
# app.run(host = '0.0.0.0', port = 5000) # 使操作系统监听所有公网 IP
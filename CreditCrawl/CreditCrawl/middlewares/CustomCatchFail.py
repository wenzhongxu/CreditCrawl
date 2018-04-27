# -*- coding: utf-8 -*-
# @Time    : 2018/4/27 10:18
# @Author  : XuWenzhong
# @Email   : xuwenzhong1994@163.com
# @File    : CustomCatchFail.py
# @Version : 1.0.1
# @Software: PyCharm

import urllib2
import urllib
import logging


class CatchFailMiddleware(object):
    def __init__(self, xcrs_host, xcrs_port):
        self.xcrs_host = xcrs_host
        self.xcrs_port = xcrs_port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            xcrs_host=crawler.settings.get('XCRS_HOST'),
            xcrs_port=crawler.settings.get('XCRS_PORT')
        )

    def process_response(self, request, response, spider):
        if response.status >= 400:
            # reason = response_status_message(response.status)
            reason = "目标网址解析异常"
            self.sendfail(request, reason, spider)
        return response

    def process_exception(self, request, exception, spider):
        self.sendfail(request, exception, spider)
        return request

    def sendfail(self, reason, spider):
        data = dict()
        data["SITE_NAME"] = spider.rule["sitename"].encode("utf8")
        data["SITE_URL"] = spider.start_urls
        data["LOG_CONTENT"] = reason
        objjson = urllib.urlencode(data).encode(encoding="UTF8")
        headers = {
            'content-Type': 'application/x-www-form-urlencoded'
        }
        requrl = "http://%s:%s/PublicOpinion/PublicOpinionAjaxAPI.asmx/AddTpboLog" % (self.xcrs_host, self.xcrs_port)
        try:
            req = urllib2.Request(url=requrl, headers=headers, data=objjson)
            res_data = urllib2.urlopen(req)
            res = res_data.read()
            logging.info(res)
        except Exception as e:
            raise e

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from tools import myUtil


class UniversalcrawlPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'xcrs_test')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        document = dict(item)
        print(document)
        try:
            self.db.info_detail.insert(doc_or_docs=document, continue_on_error=True)
        except pymongo.errors.DuplicateKeyError:
            pass
        print "--isfilter---" + document["isfilter"]
        if document["isfilter"] == "是" and myUtil.iscontainkeywords(document['_id']):
            try:
                self.db.info_detail4email.insert(doc_or_docs=document, continue_on_error=True)
            except pymongo.errors.DuplicateKeyError:
                pass
        else:
            pass
        return item

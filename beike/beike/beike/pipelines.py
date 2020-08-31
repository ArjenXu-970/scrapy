# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.item import Item
import pymongo


class BeikePipeline(object):
    def process_item(self, item, spider):
        return item

class MongoDBPipeline(object):
	DB_URI="mongodb://122.228.208.83:XXXXX"
	DB_NAME="beike_deal"

	def open_spider(self,spider):
		self.client=pymongo.MongoClient(self.DB_URI)
		self.db=self.client[self.DB_NAME]

	def close_spider(self,spider):
		self.client.close()

	def process_item(self,item,spider):
		collection=self.db[spider.name]
		post=dict(item) if isinstance(item.Item) else item
		collection.insert_one(post)
		return item






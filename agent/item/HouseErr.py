#!/usr/bin/python
# -*-coding:utf-8-*-
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy


class HouseErr(scrapy.Item):
    # 主健(完整的URL md5)
    _id = scrapy.Field()
    status = scrapy.Field()
    # 类型 SaleHouse  SaleVilla  SaleOffice  SaleShop
    type = scrapy.Field()
    # 访问URL
    urls = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 网站
    site = scrapy.Field()

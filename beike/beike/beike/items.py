# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BeikeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id=Field()
    city=Field()
    ver=Field()
    zone=Field()
    site=Field()
    flag=Field()
    street=Field()
    urls=Field()
    typ=fields()




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


class Agent(scrapy.Item):
    # 主健(完整的URL md5)
    _id = scrapy.Field()
    # 发布人
    name = scrapy.Field()
    # 联系方式
    tel = scrapy.Field()
    # 联系方式
    contact = scrapy.Field() 
    # 公司
    staffNo = scrapy.Field()
    # 门店
    stores = scrapy.Field()
    # 门店
    zone = scrapy.Field()
    # 门店
    street = scrapy.Field()
    # 地图
    mapX = scrapy.Field()
    # 地图
    mapY = scrapy.Field()
    # 职位
    position = scrapy.Field()
    # 入职链家
    entry = scrapy.Field()
    # 个人成绩
    score = scrapy.Field()
    # 访问URL
    urls = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 网站
    site = scrapy.Field()
    # 类型
    type = scrapy.Field()
    # 位于
    address = scrapy.Field()
    # 针对58处理
    source = scrapy.Field()
    # 近30天成交
    score_30 = scrapy.Field()

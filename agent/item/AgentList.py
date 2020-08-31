#!/usr/bin/python
#-*-coding:utf-8-*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy
class AgentList(scrapy.Item):
    #主健(完整的 md5)
    _id = scrapy.Field()
    #类型
    type = scrapy.Field()
    #关键字
    keys = scrapy.Field()
    #完整URL
    url = scrapy.Field()
    #网站
    site = scrapy.Field()
    #城市
    city = scrapy.Field()
    #采集时间
    spidertime= scrapy.Field()
    #联系方式
    contact = scrapy.Field()
    # 公司
    staffNo = scrapy.Field()
    # 门店
    stores = scrapy.Field()
    # 发布人
    name = scrapy.Field()

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
class HouseSale(scrapy.Item):
        #主健(完整的URL md5)
        _id = scrapy.Field()
        #类型 SaleHouse  SaleVilla  SaleOffice  SaleShop
        type = scrapy.Field()
        #标题
        title = scrapy.Field()
        # 总价 (只保留数字 默认单位万元)
        total = scrapy.Field()
        # 户型
        room = scrapy.Field()
        # 建筑面积 (只保留数字 默认单位平米)
        area = scrapy.Field()
        # 建筑年代 (只保留数字 默认单位年)
        years = scrapy.Field()
        # 朝向
        towards = scrapy.Field()
        # 总楼层 (只保留数字 默认单位层)
        floors = scrapy.Field()
        # 当前楼层 (只保留数字 默认单位层 特殊情况可留汉字)
        floor = scrapy.Field()
        # 结构
        structure = scrapy.Field()
        # 装修
        decoration = scrapy.Field()
        # 物业类别
        property = scrapy.Field()
        # 建筑类别
        building = scrapy.Field()
        # 产权性质
        equity = scrapy.Field()
        # 楼盘名称
        comm = scrapy.Field()
        # 区域
        zone = scrapy.Field()
        # 街道
        street = scrapy.Field()
        # 配套设施
        support = scrapy.Field()
        # 房源编号(对方网站编号)
        listings1 = scrapy.Field()
        #内部编号
        listings2 = scrapy.Field()
        # 标签
        tag = scrapy.Field()
        #成交
        clinch = scrapy.Field()
        #经纪人房评
        review = scrapy.Field()
        #客户看房数
        showings = scrapy.Field()
        showings2 = scrapy.Field()
        # 发布时间
        addtime = scrapy.Field()
        # 采集时间
        spidertime = scrapy.Field()
        # 成交时间
        dealtime = scrapy.Field()
        #各种特点
        #------------------写字楼-----------------------------------
        # 等级
        grade = scrapy.Field()
        # 是否可分割
        excision = scrapy.Field()
        # 得房率(默认单位% 保留完整单位)
        rate = scrapy.Field()
        # 配套设施(已存在)
        #support = scrapy.Field()
        # 物业费
        costs = scrapy.Field()
        #-----------------------------商铺---------------------------
        # 是否可分割(已存在)
        #excision = scrapy.Field()
        # 得房率(已存在)
        #rate = scrapy.Field()
        # 配套设施(已存在)
        #support = scrapy.Field()
        # 物业费(已存在)
        #costs = scrapy.Field()
        #商铺特征
        feature = scrapy.Field()
        #目标业态
        Format = scrapy.Field()
        #------------------------------别墅--------------------------
        # 进门朝向(已存在)
        #towards = scrapy.Field()
        # 地上层数(已存在)
        #floor = scrapy.Field()
        # 建筑形式(已存在)
        #building = scrapy.Field()
        # 花园面积(只保留数字 默认单位平米)
        garden = scrapy.Field()
        # 厅结构
        hall = scrapy.Field()
        # 车库数量(只保留数字 默认单位个)
        garage = scrapy.Field()
        # 车位数量(只保留数字 默认单位个)
        parking = scrapy.Field()
        # 地下室面积(只保留数字 默认单位平米)
        basement = scrapy.Field()
        # 地下室明暗状态
        shading = scrapy.Field()
        #------------------------房源发布人信息---------------------------
        # 发布人
        name = scrapy.Field()
        # 联系方式
        contact = scrapy.Field()
        # 员工ID
        staffNo = scrapy.Field()
        # 公司
        company = scrapy.Field()
        # 门店
        stores = scrapy.Field()
        # 访问URL
        urls = scrapy.Field()
        # 城市
        city = scrapy.Field()
        # 网站
        site = scrapy.Field()



# -*- coding:utf-8 -*-
import scrapy 
from urlparse import urljoin
import hashlib

def encode(text):
	h1=hashlib.md5()
	h1.update(text)
	return h1.hexdigest()

class city_list(scrapy.Spider):
	name="city"

	# start_urls=["https://www.ke.com/city/"]

	def start_requests(self):
		yield scrapy.Request("https://www.ke.com/city/",callback=self.parse_all,dont_filter=False)

	def parse_all(self,response):
		for content in response.xpath("//ul[@class='city_list_ul']//li[contains(@data-action,'''国内''')]"):
			city=content.xpath("./text()")
			urls="https://"+content.xpath(".//a/@href")+"chengjiao/"
			print(city)
			yield scrapy.Requests(url=urls,callback=self.parse_city,meta={"city":city},dont_filter=False)

	def parse_city(self,response):
		if response.status==200:
			city=reponse.meta["city"]
			for content in response.xpath("//div[@data-role='ershoufang']//a"):
				url=content.xpath("./@href")
				urls=urljoin(response.url,url)
				district=content.xpath("./text()")
				yield scrapy.Request(url=urls,callback=self.parse_district,meta={"city":city,"district":district},dont_filter=False)
		else:
			pass

	def parse_district(self,response):
		if response.status==200:
			city=response.meta["city"]
			district=response.meta["district"]
			for content in response.xpath("//div[@data-role='ershoufang']/div[2]/a"):
				item=BeikeItem()
				url=content.xpath("./@href")
				item["urls"]=urljoin(response.url,url)
				item["street"]=content.xpath("./text()")
				item["city"]=city
				item["zone"]=district
				item["site"]="beike"
				item["typ"]="deal"
				item["ver"]="v1"
				item["_id"]=encode(item["urls"])
				print(district)
		else:
			return 0








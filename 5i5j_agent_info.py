# -*- coding:utf-8 -*-
import requests
import pymongo
import random
import hashlib
from bs4 import BeautifulSoup
from scrapy.selector import Selector

USER_AGENTS = [
    {"User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)"},
    {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)"},
    {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)"},
    {"User-Agent": "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)"},
    {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)"},
    {"User-Agent": "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)"},
    {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)"},
    {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)"},
    {"User-Agent": "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6"},
    {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1"},
    {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0"},
    {"User-Agent": "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"},
    {"User-Agent": "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20"},
    {"User-Agent": "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52"},
]

thread_num=10

def connnect_mongo():
    mongo_uri = [
        "mongodb://admin:XXXXX@192.168.0.13:XXXXX",
        "mongodb://admin:XXXXX@192.168.0.14:XXXXX"]
    con = pymongo.MongoClient(host=mongo_uri, replicaSet="big_data3")
    db = con['task']
    return db

def random_header(USER_AGENTS):
	return random.choice(USER_AGENTS)

def get_from_mongo():
	date=connnect_mongo()
	for info in date["agent_m5i5j"].find():
		url=info["urls"]
		city=info["city"]
		get_detail(url,city)

def get_stores(string):
	ll=string.split(" · ")
	if len(ll)==4:
		return ll[2]
	if len(ll)==2:
		return ll[0]

def get_zone(string):
	ll=string.split(" · ")
	if len(ll)==4:
		return ll[0]
	if len(ll)==2:
		return 0

def get_street(string):
	ll=string.split(" · ")
	if len(ll)==4:
		return ll[1]
	if len(ll)==2:
		return 0

def MD5(text):
    h1 = hashlib.md5()
    h1.update(text)
    return h1.hexdigest()

def get_score(string):
	return string.split("(")[1].split(")")[0]

def get_entry(string):
	return string.split(" · ")[-1]

def get_detail(url,city):
	details={}
	header=random_header(USER_AGENTS)
	content=requests.get(url=url,headers=header)
	soup=Selector(text=content.text)
	for infos in soup.xpath("//div[@class='list-con-box']/div"):
		addr=infos.xpath(u"//p[@class='iconsleft']/text()").extract_first()	
		details["city"]=city
		details["stores"]=get_stores(addr)
		details["name"]=infos.xpath(u"//h3/text()").extract_first()
		details["zone"]=get_zone(addr)
		details["staffNo"]="5i5j"
		details["site"]="5i5j"
		details["contact"]=infos.xpath(u"//div[@class='contacty']/span/text()").extract_first()
		details["score"]=get_score(info.xpath(u"//p[@class='iconsleft1']/text").extract_first())
		details["street"]=get_street(addr)
		details["urls"]=u"https://bj.5i5j.com"+infos.xpath(u"//div[@class='agent-tit']/a[1]/@href").extract_first()
		details["entry"]=get_entry(addr)
		details["_id"]=MD5(details["urls"])
		details["type"]="Agent"
		print(details)

url="https://bj.5i5j.com/jingjiren/chaoyangqu/n1/"
city="beijing"
get_detail(url,city)
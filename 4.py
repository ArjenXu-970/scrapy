import requests
from bs4 import BeautifulSoup
from urlparse import urljoin
import hashlib
import os
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

def encode(text):
	h1=hashlib.md5()
	h1.update(text)
	return h1.hexdigest()


def get_roads(url,city_name,zone_name):
	header={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome}",
			"Accept-Encoding":"gzip, deflate, br"}
	r=requests.get(url=url,headers=header)
	print(r.status_code)
	content=BeautifulSoup(r.text,"lxml")
	num=content.find("div",attrs={'class':"total-box"}).find("span").text
	if num==0:
		return 0
	else:
		if int(num)%30==0:
			page_num=int(num)//30
		else:
			page_num=int(num)//30+1
	with open("data.txt","a") as f:
		for s in range(1,page_num+1):
			urls=url+"n%d/"%s
			ids=encode(urls)
			f.write(ids+"-"+city_name+"-"+zone_name+"-"+urls)
			f.write("\r\n")
	# print(road.text.strip())
	# print(urljoin(url,road["href"]))
	# wangzhi=urljoin(url,road["href"])
	print(int(num),page_num)
url="https://bj.5i5j.com/jingjiren/fangshanqu/"
# get_roads(url,"bj","pg")

def start_crawl(path):
	r=os.listdir(path)
	print(unicode(r[0],"utf-8"))
	b=r[0].encode
	# with open(unicode(path+"/"+r[0],"utf-8"),"r") as f:
	# 	for line in f:
	# 		print(line) 
	# for file in r:
		
		

start_crawl("cities")


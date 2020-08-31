import requests
from bs4 import BeautifulSoup
from urlparse import urljoin
import sys
import hashlib
import pymongo
reload(sys)
sys.setdefaultencoding('utf-8')
host="192.168.0.13"
port=XXXXX
account="admin"
passward="XXXXX"
data=[]
cities_link=[]
regions_link=[]

# def connect(host,port,passward,account):
# 	client=pymongo.MongoClient("mongodb://%s:%s@%s:%d"%(account,passward,host,port))
# 	db=client["task"]
# 	collection=db["agent_5i5j"]


def encode(text):
	h1=hashlib.md5()
	h1.update(text)
	return h1.hexdigest()

def get_zhu_html(url):
	print("hello")
	header={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome}",
			}
	
	r=requests.get(url=url,timeout=30,headers=header)
	print(r.status_code)
	print(r.encoding)
	r.encoding = 'utf-8'
	# r.encoding=r.apparant_encoding
	return r.text

def get_chengshi_url(url):
	content=get_zhu_html(url)
	soup=BeautifulSoup(content,"lxml")
	for city in soup.find_all("p",attrs={'class':"city fl"}):
		name=city.find("a").text
		link=city.find("a")["href"]+"jingjiren/"
		cities_link.append(link)

def get_chengshi_html(url):
	header={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome}",
			}
	r=requests.get(url,headers=header)
	print(r.status_code)
	return r.text
	
def get_qu_url(url):
	content=get_chengshi_html(url)
	soup=BeautifulSoup(content,"lxml")
	for qu in soup.find("ul",attrs={'class':'''new_di_tab sTab'''}).find_all("a")[1:]:  
		link=urljoin(url,qu["href"])
		name=qu.find("li").text.strip()
		regions_link.append(link)
	
def get_info(url,collection):
	header={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome}",
			}
	r=requests.get(url,headers=header)
	soup=BeautifulSoup(r.text,"lxml")
	num=soup.find("div",attrs={'class':"total-box"}).find("span").text
	city=soup.find("div",attrs={'class':'top-city'}).text.strip()
	zone=soup.find_all("div",attrs={'class':"tCon"})[1].find("span").text.strip()
	if num==0:
		return 0
	else:
		if int(num)%30==0:
			page_num=int(num)//30
		else:
			page_num=int(num)//30+1
	for i in range(1,page_num+1):
		urls=url+"n%d"%i+"/"
		ids=encode(urls)
		dict={"_id":ids,"city":city,"ver":"v1","zone":zone,"site":"5i5j","urls":urls,"type":"agent"}
		collection.insert_one(dict)

def run(url,account,passward,host,port):
	client=pymongo.MongoClient("mongodb://%s:%s@%s:%d"%(account,passward,host,port))
	db=client["task"]
	collection=db["agent_5i5j"]
	get_chengshi_url(url)
	for link in cities_link:
		get_qu_url(link)
	for lianjie in regions_link:
		get_info(lianjie,collection)

url="https://sh.5i5j.com/jingjiren/"
run(url,account,passward,host,port)

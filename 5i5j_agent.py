# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
from urlparse import urljoin
import sys
import math, time
import hashlib
import pymongo
from scrapy.selector import Selector
from fake_useragent import FakeUserAgent

reload(sys)
sys.setdefaultencoding('utf-8')

header = {'User-Agent': FakeUserAgent().random, }

data = []
cities_link = []
regions_link = []


def mongo13():
    mongo_uri = [
        "mongodb://admin:XXXXX@192.168.0.13:XXXXX",
        "mongodb://admin:XXXXX@192.168.0.14:XXXXX"]
    con = pymongo.MongoClient(host=mongo_uri, replicaSet="big_data3")
    db = con['task']
    return db


def MD5(text):
    h1 = hashlib.md5()
    h1.update(text)
    return h1.hexdigest()


def get_chengshi_html(url):
    r = requests.get(url, headers=header)
    return r.text


def get_chengshi_url(url):
    content = get_chengshi_html(url)
    soup = BeautifulSoup(content, "lxml")
    for city in soup.find_all("p", attrs={'class': "city fl"}):
        link = city.find("a")["href"] + "jingjiren/"
        cities_link.append(link)


def get_qu_url(url):
    content = Selector(text=get_chengshi_html(url))
    xpaths = content.xpath("//ul[@class='new_di_tab sTab']/a[position()>1]")
    if xpaths:
        for list in xpaths:
            urls = list.xpath("./@href").extract_first()
            link = urljoin(url, urls)
            regions_link.append(link)


def get_info(url):
    info = {}
    content = Selector(text=get_chengshi_html(url))
    info['city'] = content.xpath(u"//div[@class='top-city']/text()").extract_first()
    info['zone'] = content.xpath(u"//div[contains(text(),'条件')]/following-sibling::div/span/text()").extract_first()
    pag = content.xpath(u"//div[contains(text(),'共找到')]/span/text()").extract_first()
    if pag:
        pag = int(pag)
        page = int(math.ceil(float(pag) / 30)) + 1
        for i in range(1, page):
            info['urls'] = url + 'n%s/' % i
            info['type'] = 'agent'
            info['ver'] = 'V1'
            info['site'] = 'm5i5j'
            info['spidertime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            info['_id'] = MD5(info['urls'])
            print info['_id']
            mongo13()['agent_m5i5j'].save(info)


def run(url):
    get_chengshi_url(url)
    for link in cities_link:
        get_qu_url(link)
    for lianjie in regions_link:
        get_info(lianjie)


if __name__ == "__main__":
    url = "https://sh.5i5j.com/jingjiren/"
    run(url)

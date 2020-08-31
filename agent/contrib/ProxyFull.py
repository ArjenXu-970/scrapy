#!/usr/bin/python
# -*-coding:utf-8-*-

import pymysql
import time

from twisted.internet import defer
from twisted.internet.error import TimeoutError, DNSLookupError, \
    ConnectionRefusedError, ConnectionDone, ConnectError, \
    ConnectionLost, TCPTimedOutError
from twisted.web.client import ResponseFailed
from scrapy.utils.response import response_status_message


class ProxyMiddleware(object):
    EXCEPTIONS_TO_RETRY = (defer.TimeoutError, TimeoutError, DNSLookupError,
                           ConnectionRefusedError, ConnectionDone, ConnectError,
                           ConnectionLost, TCPTimedOutError, ResponseFailed,
                           IOError)

    # 遇到这些类型的错误直接当做代理不可用处理掉, 不再传给retrymiddleware
    def __init__(self, settings):
        # 系统默认配置文件
        self.settings = settings
        # 默认0不需要用代理的情况，其它增量添加
        self.proxyes = ['localhost'];

        # self.index=-1
        self.index = 0
        self.lastTime = 0

        self.retry_http_codes = set(int(x) for x in settings.getlist('RETRY_HTTP_CODES'))
        self.retry_times = int(settings.get("RETRY_TIMES", 3))

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    # 代理补入
    def fetch_new_proxyes(self):
        mysqlset = self.settings.getdict("PROXY_MYSQL")
        conn = pymysql.connect(
            host=mysqlset['Host'],
            port=mysqlset['Port'],
            user=mysqlset['User'],
            passwd=mysqlset['Passwd'],
            db=mysqlset['Db'],
            charset=mysqlset['Charset']
        )
        cur = conn.cursor(pymysql.cursors.DictCursor)

        cur.execute(
            "Select `ip`  From tmpipfull Where `speed`=1 and UNIX_TIMESTAMP(`Time`)>(SELECT UNIX_TIMESTAMP(max(`Time`)) FROM  tmpipfull)-60  order by RAND() LIMIT 20 ")
        for r in cur:
            ips = "http://" + r['ip']
            if ips not in self.proxyes:
                self.proxyes.append(ips)
        cur.close()
        conn.close()
        self.lastTime = time.time()

    def process_request(self, request, spider):
        if hasattr(spider, "Dont_HttpProxy") and spider.Dont_HttpProxy == True:
            return
        # 如果进入重试环节,则清理上次IP
        # 20次以内用付费IP
        retries = int(request.meta.get('retry_times', 0))
        if retries < 4 or retries % 3 == 0:
            return

        # IP可用水位
        if len(self.proxyes) < self.settings.get("PROXY_MIN_NUM", 10):
            self.fetch_new_proxyes();
        # 超时时间
        if (time.time() - self.lastTime) > 60:
            self.fetch_new_proxyes();
        # IP正常
        if (len(self.proxyes) > 1):
            self.index = (self.index + 1) % len(self.proxyes)
        else:
            self.index = 0
        proxy = self.proxyes[self.index]

        if proxy != 'localhost':
            request.meta["proxy"] = proxy
            # request.meta["dont_redirect"] = True
        elif "proxy" in request.meta.keys():
            del request.meta["proxy"]

#!/usr/bin/python
# -*-coding:utf-8-*-

import pymysql
import time
import random
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
        self.proxyes = ['localhost']
        self.proxids = {}
        # self.index=-1
        self.index = 0
        self.lastTime = 0

        self.retry_http_codes = set(int(x) for x in settings.getlist('RETRY_HTTP_CODES'))
        self.retry_times = int(settings.get("RETRY_TIMES", 3))
        self.priority_adjust = settings.getint('RETRY_PRIORITY_ADJUST')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    # 代理补入
    def fetch_new_proxyes(self,spider):
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

        # 随机读取code值;
        # code = [1, 2, 3, 5, 7]
        # random.shuffle(code)
        # code = random.choice(code)

        if 'anjuke' in spider.name:
            code = 6

        cur.execute("Select `SNO`,`ip` From tmpfree Where `speed`=1 and `Code`=%d LIMIT 20" % code)
        # cur.execute("Select `SNO`,`ip` From tmpfree Where `speed`=1")
        for r in cur:
            ips = "http://" + r['ip']
            print ips, '>>>>>>>>>>>>'
            if ips not in self.proxyes:
                self.proxyes.append(ips)
                self.proxids[ips] = r['SNO']
        cur.close()
        conn.close()
        self.lastTime = time.time()

    def process_request(self, request, spider):
        if hasattr(spider, "Dont_HttpProxy") and spider.Dont_HttpProxy == True:
            return
        # 如果进入重试环节,则清理上次IP
        retries = int(request.meta.get('retry_times', 0))
        # 20次以内用付费IP 20次以上用免费
        if (retries > 3):
            if (retries % 3 != 0):
                return
        # IP可用水位
        if len(self.proxyes) < self.settings.get("PROXY_MIN_NUM", 5):
            self.fetch_new_proxyes(spider)
        # 超时时间
        if (time.time() - self.lastTime) > 100:
            self.fetch_new_proxyes(spider)
        # IP正常
        if (len(self.proxyes) > 1):
            self.index = (self.index + 1) % len(self.proxyes)
        else:
            self.index = 0
        proxy = self.proxyes[self.index]

        if proxy != 'localhost':
            request.meta["proxy"] = proxy
            request.meta["SNO"] = self.proxids.get(str(proxy), 'None')
            # request.meta["dont_redirect"] = True
        elif "proxy" in request.meta.keys():
            del request.meta["proxy"]
            try:
                del request.meta["SNO"]
            except:
                pass

    def retry_request(self, request, reason, spider):
        proxy = request.meta.get('proxy', 'None')
        proxid = request.meta.get('SNO', 'None')
        if "proxy" in request.meta.keys():
            try:
                self.proxyes.remove(request.meta.get('proxy'))
                del self.proxids[str(proxy)]
            except:
                pass
        retries = int(request.meta.get('retry_times', 0)) + 1
        if retries < self.retry_times:
            spider.logger.info("Retrying %(request)s %(proxy)s %(Proxid)s (failed %(retries)d times): %(reason)s",
                               {'request': request, 'proxy': proxy, 'Proxid': proxid, 'retries': retries,
                                'reason': reason},
                               extra={'spider': spider})
            new_request = request.copy()
            # URL排重去了.不然重试无效
            new_request.dont_filter = True
            new_request.meta['retry_times'] = retries
            new_request.priority = -(abs(request.priority) + self.priority_adjust)
            if "proxy" in new_request.meta.keys():
                del new_request.meta["proxy"]
                try:
                    del new_request.meta["SNO"]
                except:
                    pass
            return new_request

    def process_response(self, request, response, spider):
        """
        检查response.status, 根据status是否在允许的状态码中决定是否切换到下一个proxy, 或者禁用proxy
        """
        spider.logger.info("None %s %s %s [RE %s] %s" % (
        request.meta.get('proxy', ''), request.meta.get('SNO', 'None'), response.status,
        request.meta.get('retry_times', 0), response.url))
        http_codes = self.retry_http_codes
        if hasattr(spider, "ReHttpStatus_Code"):
            http_codes.update(set(int(x) for x in spider.ReHttpStatus_Code))
        Re_URl = False
        if hasattr(spider, "ReHttp_Url_Content"):
            if spider.ReHttp_Url_Content in response.url:
                Re_URl = True
        if response.status in http_codes or Re_URl:
            reason = response_status_message(response.status)
            return self.retry_request(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):

        if isinstance(exception, self.EXCEPTIONS_TO_RETRY):
            return self.retry_request(request, exception, spider)

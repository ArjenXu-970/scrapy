#!/usr/bin/python
# -*-coding:utf-8-*-
import pika


class RabbitMqLog(object):
    # 遇到这些类型的错误直接当做代理不可用处理掉, 不再传给retrymiddleware
    def __init__(self, settings, channel):
        # 系统默认配置文件
        self.settings = settings;
        self.channel = channel;

    # @classmethod
    # def from_settings(cls, settings):
    #     _set=settings.getdict("RABBITMG")
    #     dels = pika.PlainCredentials(_set['User'],_set['Passwd'])
    #     conn = pika.BlockingConnection(pika.ConnectionParameters(_set['Host'],int(_set['PORT']),'/',dels))
    #     channel = conn.channel()
    #     return cls(settings, channel=channel)
    # @classmethod
    # def from_crawler(cls, crawler):
    #     return cls.from_settings(crawler.settings)
    def process_response(self, request, response, spider):
        return response
        # res={
        #     'SNO':request.meta.get('SNO', 'None'),
        #     'IP':request.meta.get('proxy', ''),
        #     'status':response.status,
        #     'retry_times':request.meta.get('retry_times', 0),
        #     'url':response.url
        # }
        # self.channel.queue_declare(queue=spider.name)
        # self.channel.basic_publish(exchange='',routing_key=spider.name,body=str(res))
        # return response

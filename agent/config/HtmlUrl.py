#!/usr/bin/python
#-*-coding:utf-8-*-
def Geturl(url):
    url=url.split("#")[0]
    # if url[-1]!='/':
    #     url+='/'
    return  url

def Getkeys(url):
    return  Geturl(url).split("/")[-2]

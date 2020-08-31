#!/usr/bin/python
#-*-coding:utf-8-*-
import hashlib
def MD5(src):
    m2 = hashlib.md5()
    m2.update(src)
    return m2.hexdigest()

#print MD5("http://sh.esf.sina.com.cn/detail/65274344/")
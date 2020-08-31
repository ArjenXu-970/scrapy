#!/usr/bin/python
#-*-coding:utf-8-*-
import re
def HtmlRePat(nbody,xbody,Xml):
        if Xml['xml']=="xpath":
            rs = xbody.xpath(Xml['pat']).extract()
        elif Xml['xml']=="re":
            rs_=re.compile(Xml['pat'], re.S|re.I).findall(nbody)
            rs=[]
            if rs_:
                for x in rs_:
                    rs.append(x.decode(Xml["code"],'ignore').encode('utf-8'))
        else:
            rs=[]
            rs.append(Xml['pat'])
        return  rs

#!/usr/bin/env python
#coding=utf-8

import os
import config

'''私有函数, 抓取地址为url的数据'''
def __crawl(url, user_agent, cookie):
    return os.popen("http --check-status --timeout=2 -b '" + url + "' User_Agent:'" + user_agent + "' Cookie:'" + cookie + "'").read()

'''抓取新浪微博数据'''
def crawl_weibo(url):
    return __crawl(url, config.USER_AGENT, config.COOKIE)

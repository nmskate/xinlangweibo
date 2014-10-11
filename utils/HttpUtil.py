#!/usr/bin/env python
#coding=utf-8

import os
import config

'''私有函数, 抓取地址为url的数据'''
def __crawl(url, user_agent, cookie):
    return os.popen("http --check-status --timeout=5 -b '" + url + "' User_Agent:'" + user_agent + "' Cookie:'" + cookie + "'").read()

'''私有函数，获取请求地址为url的请求响应头'''
def __crawl_head(url, user_agent, cookie):
    return os.popen("http --timeout=3 -v HEAD '" + url + "' User_Agent:'" + user_agent + "' Cookie:'" + cookie + "' 2>/dev/null").read()

'''抓取新浪微博数据'''
def crawl_weibo(url):
    return __crawl(url, config.USER_AGENT, config.COOKIE)

def correct_weibo_head(url):
    return __crawl_head(url, config.USER_AGENT, config.COOKIE).find('200 OK') >= 0

#!/usr/bin/env python
#coding=utf-8

'''新浪微博域'''
BASE_URL = "http://weibo.com"

'''模拟浏览器, 默认浏览器:firefox 31.0, 操作系统: Ubuntu x86_64'''
USER_AGENT = '''Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0'''

'''请求时所带的cookie'''
COOKIE = '''TC-Page-G0=444eec11edc8886c2f0ba91990c33cda; SUB=_2AkMjXiBXf8NjqwJRmPkXzGPgb4p2yA3EiebDAHzsJxJjHm407CNWlpVhFEtVcQTevPNbEBd2R7Xe;SUBP=0033WrSXqPxfM72-Ws9jqgMF55z29P9D9WWG0Ow7-zgdGSQb8RvgfJJB; _s_tentry=passport.weibo.com; Apache=5164208644005.779.1409462121774;SINAGLOBAL=5164208644005.779.1409462121774; ULV=1409462121800:1:1:1:5164208644005.779.1409462121774:; TC-Ugrow-G0=370f21725a3b0b57d0baaf8dd6f16a18; TC-V5-G0=5fc1edb622413480f88ccd36a41ee587'''

'''新浪微博按名字搜索的基础地址'''
BASE_URL_NAME_SEARCH = "http://s.weibo.com/weibo/"

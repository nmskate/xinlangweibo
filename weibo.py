#!/usr/bin/env python
#coding=utf-8

from utils import crawl
import config
import urllib2

class Weibo:

    '''生成按名字搜索的页面地址'''
    @classmethod
    def gen_name_url(cls, name):
        return config.BASE_URL_NAME_SEARCH + urllib2.quote(urllib2.quote(name).encode()).encode()

    '''获取按名字搜索页面中的真实地址'''
    @classmethod
    def get_real_name_url(cls, url):
        pass


if __name__ == "__main__":
    html = crawl.crawl_weibo("http://s.weibo.com/weibo/%25E8%258B%25B1%25E5%259B%25BD%25E6%258A%25A5%25E5%25A7%2590")
    print html

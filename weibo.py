#!/usr/bin/env python
#coding=utf-8

from utils import crawl
from model import weibodata
import config
import urllib2

class Weibo:

    '''抓数据主函数'''
    @classmethod
    def do_weibo(cls, names):
        weibo_data_all = []
        for name in names:
            weibo_data = weibodata.WeiboData()

            #微博名的搜索地址
            name_url = cls.__gen_name_url(name)

            html_contain_real_home_url = crawl.crawl_weibo(name_url)
            #用户的微博主页地址
            real_home_url = cls.__get_real_home_url(html_contain_real_home_url)

            html_weibo_home = crawl.crawl_weibo(real_home_url)
            #微博主页中的'微博'标签页地址
            real_weibo_url = cls.__get_real_weibo_url(html_weibo_home)

            html_real_weibo_url = crawl.crawl_weibo(real_weibo_url)
            print html_real_weibo_url
            
            #解析'微博'标签页中的数据
            weibo_data = cls.__fetch_data(html_real_weibo_url)

    '''生成按名字搜索的页面地址'''
    @classmethod
    def __gen_name_url(cls, name):
        if name == '':
            raise Exception, '1'
        return config.BASE_URL_NAME_SEARCH + urllib2.quote(urllib2.quote(name).encode()).encode()

    '''获取按名字搜索页面中的真实地址'''
    @classmethod
    def __get_real_home_url(cls, real_home_html):
        try:
            href_start = real_home_html.find('href', real_home_html.find('person_name'))
            href_end = real_home_html.find(' ', href_start + 1)
            href_all = real_home_html[href_start : href_end]
            return (href_all[href_all.find('=') + 1 :]).replace("\\", '').strip("=\"")
        except:
            raise Exception, '2'

    '''获取用于微博主页的'微博'标签页地址'''
    @classmethod
    def __get_real_weibo_url(cls, real_name_url):
        try:
            start = real_name_url.find('pftb_itm S_line1')
            end = real_name_url.find('微博', start)
            tmp = real_name_url[(start + 1) : end]
            real_weibo_url = ''
            for i in range(1000):
                start = tmp.find('pftb_itm S_line1')
                if start == -1:
                    href = tmp[tmp.find('href') : end]
                    href = href[href.find('=') : href.find(' ')]
                    real_weibo_url = config.BASE_URL + href.replace("\\", '').strip("=\"")
                    break
                else:
                    tmp = tmp[(start + 1) : end]
            return real_weibo_url
        except:
            raise Exception, '3'

    '''获取微博的数据'''
    @classmethod
    def __fetch_data(cls, html_weibo):
        pass

if __name__ == "__main__":
    Weibo.do_weibo(['英国报姐'])

#!/usr/bin/env python
#coding=utf8

import config
import urllib2
import time

'''生成微博url'''
def gen_name_url(name):
    return "http://s.weibo.com/weibo/" + urllib2.quote(urllib2.quote(name).encode()).encode()

def search_data(driver, name):
    '''先根据中文名生成微博的查询地址'''
    driver.get(gen_name_url(name))
    time.sleep(config.WAIT_TIME)

    '''查询真实url'''
    pl_weibo_directtop = driver.find_element_by_id('pl_weibo_directtop')
    real_url = pl_weibo_directtop.find_element_by_css_selector('.person_detail .person_name a:first-child').get_attribute('href')

    '''请求真实微博主页,然后解析到微博标签地址'''
    driver.get(real_url)
    time.sleep(config.WAIT_TIME)
    weibo_url = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div[1]/div/ul/li[2]/a').get_attribute('href')

    driver.get(weibo_url)
    time.sleep(config.WAIT_TIME)
    for i in range(3):
        weibo_detail = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div[2]/div/div[1]/div/div[2]/div/div[2]/div[%d]/div/div' % (i + 1))
        zhiding_ele = weibo_detail.find_element_by_css_selector('div:first-child')
        if zhiding_ele.find_element_by_css_selector('span')

    time.sleep(config.WAIT_TIME)

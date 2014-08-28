#!/usr/bin/env python
#coding=utf8

from selenium import webdriver
import time

'''生成微博url'''
def gen_name_url(name):
    import urllib2
    return "http://s.weibo.com/weibo/" + urllib2.quote(urllib2.quote(name).encode()).encode()

'''获取微博名的真实微博地址'''
def get_real_url(name):
    #打开firefox浏览器
    driver = webdriver.Firefox()
    #请求地址
    driver.get(gen_name_url(name))
    #是否有结果
    weibo_directtop = driver.find_element_by_id("pl_weibo_directtop")
    if weibo_directtop.text.strip() == "":
        print "不能解析"
        return ""
    #提取结果
    detail_url = weibo_directtop.find_elements_by_xpath("div/div/div[1]/div[2]/p[1]/a[1]")[0].get_attribute("href")
    driver.quit()
    return detail_url

'''请求url,获取所需信息'''
def search_data(url):
    driver = webdriver.Firefox()
    driver.get(url)
    #等待3秒渲染时间
    time.sleep(5)

    weibo_tab_url = driver.find_element_by_xpath("/html/body/div/div/div/div[2]/div[1]/div/ul/li[2]/a").get_attribute("href")
    print weibo_tab_url
    #取前3条赞
    # for i in range(3):
    #     items = driver.find_elements_by_xpath("/html/body/div[1]/div/div[4]/div[2]/div[2]/div/div[1]/div/div[3]/div/div[3]/div[%d]/div/div/div[3]/div[1]/a" % (i + 1))
    #     for i in range(4):
    #         print items[i].text
    driver.quit()

    driver = webdriver.Firefox()
    driver.get(weibo_tab_url)
    #等待3秒渲染时间
    time.sleep(3)

    #取前3条赞
    for i in range(3):
        items = driver.find_elements_by_xpath("/html/body/div[1]/div/div[4]/div[2]/div[2]/div/div[1]/div/div[2]/div/div[2]/div[%d]/div/div/div[3]/div[1]/a" % (i + 1))
        for i in range(4):
            print items[i].text
    driver.quit()

search_data(get_real_url('与欧洲有关的一切'))

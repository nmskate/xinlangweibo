#!/usr/bin/env python
#coding=utf8

class Config:
    #等待时长,默认5秒
    WAIT_TIME = 5

    #微博登陆页地址
    LOGIN_PAGE_URL = "http://weibo.com/weibo"

    LOGIN_A_XPATH = "/html/body/div/div/div/div[2]/div[2]"

    #登陆页邮箱xpath
    LOGIN_EMAIL_XPATH = "/html/body/div[8]/div/div/table/tbody/tr/td/div/div[2]/div[2]/div[1]/div[1]/div/input"

    #登陆页密码xpath
    LOGIN_PASSWD_XPATH = "/html/body/div[8]/div/div/table/tbody/tr/td/div/div[2]/div[2]/div[1]/div[2]/div/input"

    #登陆页登陆按钮xpath
    LOGIN_SUBMIT_XPATH = "/html/body/div[8]/div/div/table/tbody/tr/td/div/div[2]/div[2]/div[1]/div[6]/a/span"

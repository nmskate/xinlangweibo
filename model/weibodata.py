#!/usr/bin/env python
#coding=utf-8

class WeiboItem:
    #点赞数
    zan_num = 0

    #发表时间
    send_date = ""

    #转发数
    zhuanfa_num = 0

    #评论数
    pinglun_num = 0

    #发表方式, 0代表weibo, 1代表Andriod客户端, 2代表ios客户端
    send_type = 0

class WeiboData:
    #博主名
    name = ""

    #博主主页地址
    home_url = ""

    #关注数
    guanzhu_num = 0

    #粉丝数
    fensi_num = 0

    #微博数
    weibo_num = 0

    #最近微博
    latest_weibo = []
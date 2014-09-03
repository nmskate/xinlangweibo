#!/usr/bin/env python
#coding=utf-8

class WeiboItem:

    SEND_TYPE_WEIBO = 0
    SEND_TYPE_ANDRIOD = 1
    SEND_TYPE_IPHNOE_5S = 2
    SEND_TYPE_IPHNOE = 3
    SEND_TYPE_360BROWSER = 11
    SEND_TYPE_SOUGOUBROWSER = 12
    SEND_TYPE_SHOWONE = 21

    #点赞数
    zan_num = 0

    #发表时间
    send_date = ""

    #转发数
    zhuanfa_num = 0

    #评论数
    pinglun_num = 0

    #发表方式, 0代表weibo, 1代表Andriod客户端, 2代表ios客户端
    send_type = SEND_TYPE_WEIBO

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

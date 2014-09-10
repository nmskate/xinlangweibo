#!/usr/bin/env python
#coding=utf-8

class WeiboItem:

    SEND_TYPE_WEIBO = 1
    SEND_TYPE_ANDRIOD = 2
    SEND_TYPE_IPHNOE_5S = 3
    SEND_TYPE_IPHNOE = 4
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

    DATA_STATUS_OK = 0

    DATA_STATUS_ERROR = 1

    DATA_STATUS_URL_ERROR = 2

    #博主名
    name = ""

    #excel文件中的博主名
    bozhu_excel_name = ""

    #博主主页地址
    home_url = ""

    #关注数
    guanzhu_num = 0

    #粉丝数
    fensi_num = 0

    #微博数
    weibo_num = 0

    #该微博的状态
    data_status = DATA_STATUS_OK

    #最近微博
    latest_weibo = []

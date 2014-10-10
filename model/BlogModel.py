#!/usr/bin/env python
#coding=utf-8

__author__ = 'zero.liu'


class MicroBlog:
    def __init__(self):
        #点赞数
        self.praise_num = 0

        #发表时间
        self.send_date = None

        #转发数
        self.forward_num = 0

        #评论数
        self.comment_num = 0


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

    #平均转发数
    per_zhuanfa_num = 0

    #序号
    num = 0

    #该微博的状态
    data_status = DATA_STATUS_OK

    #最近微博
    latest_weibo = []

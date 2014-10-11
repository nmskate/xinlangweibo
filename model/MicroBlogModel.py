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


class MicroBlogStatus:
    #正常
    DATA_STATUS_OK = 0

    #请求数据错误
    DATA_STATUS_DATA_ERROR = 1

    #微博主页地址错误
    DATA_STATUS_URL_ERROR = 2

    def __init__(self):
        pass


class MicroBlogHome:
    def __init__(self):
        #博主名
        self.blogger_real_name = ""

        #excel文件中的博主名
        self.blogger_excel_name = ""

        #博主主页地址
        self.home_url = ""

        #关注数
        self.follow_num = 0

        #粉丝数
        self.fans_num = 0

        #微博数
        self.micro_blog_num = 0

        #平均转发数
        self.forward_num_avg = 0

        #序号
        self.sequence = 0

        #该微博的状态
        self.data_status = MicroBlogStatus.DATA_STATUS_OK

        #最近微博
        self.latest_micro_blog = []

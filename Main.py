#!/usr/bin/env python3
#coding=utf-8

__author__ = 'zero.liu'

import MicroBlog
import Excel
import Configuration
from collections import OrderedDict
from utils import HttpClient
from datetime import datetime


INPUT_FILE = 'xml.xls'
OUTPUT_FILE = 'result_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.xls'


def init_http_client():
    #初始化HttpClient，即全局urllib2
    HttpClient(user_agent=Configuration.USER_AGENT, cookie_file='cookie.bak', init_cookie=do_login)


def do_login(cookie_file=None):
    print(cookie_file)

if __name__ == '__main__':
    #程序开始时间
    start_time = datetime.now()

    # 解析excel中的原始数据
    # excel_file = Excel.read_excel_file(INPUT_FILE)
    init_http_client()
    # # 请求每一个sheet
    # final_data = OrderedDict()
    # for sheet in excel_file.sheets:
    #     final_data[sheet.name] = MicroBlog.fetch_weibo(sheet)
    #
    # # 将结果写入文件
    # workbook = Workbook()
    # for sheet_name, item_data in final_data.items():
    #     Excel.output_weibo_data(item_data, sheet_name, workbook)
    # workbook.save(OUTPUT_FILE)

    print('共耗时：', (datetime.now() - start_time).seconds, '秒')

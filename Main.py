#!/usr/bin/env python3
# coding=utf-8

__author__ = 'zero.liu'

import os
import MicroBlog
import Excel
import Configuration
import logging
import Login

from datetime import datetime
from utils.HttpClient import HttpClient
from utils import StringUtils
from common import Charset
from collections import OrderedDict

INPUT_FILE = 'xml.xls'
OUTPUT_FILE = 'result_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.xls'
LOGGER_FILE = 'logger.log'
COOKIE_FILE = 'cookie.bak'


def init_http_client():
    # 初始化HttpClient，即全局urllib2
    HttpClient.create_http_client(user_agent=Configuration.USER_AGENT, cookie_file=COOKIE_FILE, init_cookie=Login.do_login)


def init_logging(file=LOGGER_FILE):
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=file,
                        filemode='w')


if __name__ == '__main__':
    # 程序开始时间
    start_time = datetime.now()

    # 解析excel中的原始数据
    excel_file = Excel.read_excel_file(INPUT_FILE)
    init_logging()
    init_http_client()

    html_ = HttpClient.get('http://www.weibo.com/kaifulee')
    print(StringUtils.convert_to_str(html_))
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

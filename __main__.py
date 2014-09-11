#!/usr/bin/env python
#coding=utf-8

import weibo
import excel
from xlwt import Workbook
from datetime import datetime

INPUT_FILE = '''xml.xls'''
OUTPUT_FILE = 'result_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.xls'

if __name__ == "__main__":
    start_time = datetime.now()
    #存放原始数据的excel文件
    excel_file = excel.read_excel_file(INPUT_FILE)
    #请求每一个sheet，并把结果放进excel_fiel中
    workbook = Workbook()
    for sheet_item in excel_file.sheet_items:
        weibo_all_data = weibo.Weibo.fetch_weibo(sheet_item)
        excel.output_weibo_data(weibo_all_data, sheet_item, workbook)
    workbook.save(OUTPUT_FILE)
    print '共耗时：', (datetime.now() - start_time).seconds / 60, '分钟'

#!/usr/bin/env python
#coding=utf-8

import weibo
import excel
from xlwt import Workbook
from datetime import datetime

INPUT_FILE = '''xml.xlsx'''

if __name__ == "__main__":
    #存放原始数据的excel文件
    excel_file = excel.get_excel_file(INPUT_FILE)
    #excel文件的sheet字典
    sheets_dict = excel.get_sheets_dict_from_file(excel_file)
    #请求每一个sheet，并把结果放进excel_fiel中
    workbook = Workbook()
    for sheet_name in sheets_dict.keys():
        weibo_all_data = weibo.Weibo.fetch_weibo(sheets_dict[sheet_name])
        excel.output_weibo_data(weibo_all_data, excel_file.sheet_by_name(unicode(sheet_name, "utf-8")), workbook)

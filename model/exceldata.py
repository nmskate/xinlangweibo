#!/usr/bin/env python
#coding=utf-8

class ExcelItem:

    #序号
    num = 0

    #博主名
    bozhu_name = ""

    #excel中的博主名，有些博主名后面会有一个V
    bozhu_excel_name = ""

    #链接
    link = ""

    #粉丝数/万
    fensi_num = 0

    #说明
    explain = ""

    #转发
    zhuanfa = 0

    #直发
    zhifa = 0

class SheetItem:

    #sheel名
    name = ""

    #sheel序号
    num = 0

    #序号列号
    num_index = 0

    #博主名列号
    bozhu_name_index = 0

    #链接列号
    link_index = 0

    #粉丝数/万列号
    fensi_num_index = 0

    #平均转发数列号
    per_zhuanfa_index = 0

    #说明列号
    explain_index = 0

    #转发列号
    zhuanfa_index = 0

    #直发列号
    zhifa_index = 0

    #数据
    data_items = []

    def __init__(self, num, name):
        self.num = num
        self.name = name

class Excel:

    #文件名
    name = ""

    #excel wookbook
    workbook = None

    #sheel
    sheet_items = []

    def __init__(self, name):
        self.name = name

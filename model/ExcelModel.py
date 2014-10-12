#!/usr/bin/env python3
# coding=utf-8

__author__ = 'zero.liu'

import xlrd
import os


class Row:
    def __init__(self):
        # 序号
        self.sequence = 0

        # sheet序号
        self.sheet_sequence = 0

        # 博主名
        self.blogger_real_name = ""

        # excel中的博主名，有些博主名后面会有一个V
        self.blogger_excel_name = ""

        # 链接
        self.link = ""

        # 粉丝数/万
        self.fans_num = 0

        # 平均转发数
        self.forward_num_avg = 0

        # 说明
        self.explain = ""

        # 转发
        self.forward_price = 0

        # 直发
        self.direct_send_price = 0

        # 推荐级别
        self.recommend_level = ''

        # 状态码
        self.status_code = 0


class Sheet:
    def __init__(self, sequence, name):
        # 第几个sheet
        self.sequence = sequence

        # sheet名
        self.name = name

        # 数据
        self.rows = []

        # 序号在第几列
        self.sequence_index = -1

        # 博主名在第几列
        self.blogger_name_index = -1

        # 链接在第几列
        self.link_index = -1

        # 粉丝数/万在第几列
        self.fans_num_index = -1

        # 平均转发数在第几列
        self.forward_num_avg_index = -1

        # 说明在第几列
        self.explain_index = -1

        # 转发在第几列
        self.forward_price_index = -1

        # 直发在第几列
        self.direct_send_price_index = -1

        # 推荐级别在第几列
        self.recommend_level_index = -1

        # 状态在第几列
        self.status_index = -1

        # 状态码在第几列
        self.status_code_index = -1


class Excel:
    def __init__(self, name):
        # 文件名
        self.name = name

        # excel workbook
        if os.path.exists(name):
            self.workbook = xlrd.open_workbook(name)
        else:
            self.workbook = None

        # sheets
        self.sheets = []
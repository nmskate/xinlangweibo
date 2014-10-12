#!/usr/bin/env python3
# coding=utf-8

__author__ = 'zero.liu'

import datetime
import sys
from utils import StringUtil
from model import MicroBlogModel
from model.ExcelModel import Excel, Sheet, Row


# 允许的列名
ALLOW_COLUMNS = ("序号", "类型", "博主", "账号名称", "链接", "粉丝数/万", "粉丝/万", "平均转发数",
                 "说明", "转发/元", "转发", "直发/元", "直发", "推荐级别", "状态", "状态码")


# 获取excel, 并解析出excel中的数据, 返回ExcelModel.Excel类型
def read_excel_file(input_file_name):
    excel = __check_excel_file(input_file_name)

    cur_sheet_index = 0
    for workbook_sheet in excel.workbook.sheets():
        sheet = Sheet(cur_sheet_index, workbook_sheet.name)

        sheet = __locate_col_index(sheet, workbook_sheet)

        for index in range(workbook_sheet.nrows):
            if index >= 2:
                row = Row()

                # 序号，重排序号
                row.sequence = index - 2 + 1

                # sheet序号
                row.sheet_sequence = cur_sheet_index

                # 博主名
                if sheet.blogger_name_index >= 0:
                    blogger_excel_name = str(workbook_sheet.cell(index, sheet.blogger_name_index).value).strip()
                    blogger_real_name = blogger_excel_name
                    if blogger_excel_name != "" and blogger_excel_name.endswith('V'):
                        blogger_real_name = blogger_excel_name[0: len(blogger_excel_name) - 1]
                    row.blogger_excel_name = StringUtil.strip_blank(blogger_excel_name)
                    row.blogger_real_name = StringUtil.strip_blank(blogger_real_name)

                # 链接
                if sheet.link_index >= 0:
                    link = str(workbook_sheet.cell(index, sheet.link_index).value).strip()
                    row.link = StringUtil.strip_blank(link.replace('e.weibo.com', 'weibo.com'))

                # 粉丝数/万
                if sheet.fans_num_index >= 0:
                    fans_num = str(workbook_sheet.cell(index, sheet.fans_num_index).value).strip()
                    fans_num = StringUtil.convert_to_float(fans_num)
                    row.fans_num = round(float("%.2f" % float(fans_num)), 1)

                # 平均转发数
                if sheet.forward_num_avg_index >= 0:
                    forward_num_avg = str(workbook_sheet.cell(index, sheet.forward_num_avg_index).value).strip()
                    row.forward_num_avg = StringUtil.convert_to_int(forward_num_avg, '-1')

                # 说明
                if sheet.explain_index >= 0:
                    explain = str(workbook_sheet.cell(index, sheet.explain_index).value).strip()
                    row.explain = StringUtil.strip_blank(explain)

                # 转发
                if sheet.forward_price_index >= 0:
                    forward_price = str(workbook_sheet.cell(index, sheet.forward_price_index).value).strip()
                    row.forward_price = StringUtil.convert_to_int(forward_price, '-1')

                # 直发
                if sheet.direct_send_price_index >= 0:
                    direct_send_price = str(workbook_sheet.cell(index, sheet.direct_send_price_index).value).strip()
                    row.direct_send_price = StringUtil.convert_to_int(direct_send_price, '-1')

                #推荐级别
                if sheet.recommend_level_index >= 0:
                    recommend_level = str(workbook_sheet.cell(index, sheet.recommend_level_index).value).strip()
                    row.recommend_level = StringUtil.strip_blank(recommend_level)

                # 状态码
                if sheet.status_code_index >= 0:
                    status_code = str(workbook_sheet.cell(index, sheet.status_code_index).value).strip()
                    row.status_code = StringUtil.convert_to_int(status_code)

                sheet.rows.append(row)

        excel.sheets.append(sheet)
        cur_sheet_index += 1

    return excel


# 检查输入文件格式是否正确, 正确返回文件, 错误退出
def __check_excel_file(excel_file_name):
    excel = Excel(excel_file_name)
    if isinstance(excel.workbook, type(None)):
        print(excel_file_name, '不存在，程序退出')
        sys.exit(0)

    flag = True
    for sheet in excel.workbook.sheets():
        for name in sheet.row_values(1):
            if ALLOW_COLUMNS.count(name.replace(' ', '')) == 0:
                flag = False
                print("包含有不合法的列名 --- sheet名(", sheet.name, "), 列名(", name.encode('utf-8'), ")")
                print('仅允许的列名 --- 序号, 类型, 博主, 账号名称, 链接, 粉丝数/万, 粉丝/万, 平均转发数, 说明, 转发/元, 转发, 直发/元, 直发, 推荐级别')
        if not flag:
            sys.exit(0)
        else:
            return excel


# 定位sheet中序号, 类型, 博主等等列所在的序号，其中sheet表示ExcelModel.Sheet、workbook_sheet表示workbook.sheets()中的每一个sheet
def __locate_col_index(sheet, workbook_sheet):
    cur_column = 0
    for name in workbook_sheet.row_values(1):
        name = StringUtil.strip_blank(name)
        if ["序号"].count(name) == 1:
            sheet.sequence_index = cur_column
        if ["博主", "账号名称"].count(name) == 1:
            sheet.blogger_name_index = cur_column
        if ["链接"].count(name) == 1:
            sheet.link_index = cur_column
        if ["粉丝数/万", "粉丝/万"].count(name) == 1:
            sheet.fans_num_index = cur_column
        if ["平均转发数"].count(name) == 1:
            sheet.forward_num_avg_index = cur_column
        if ["说明"].count(name) == 1:
            sheet.explain_index = cur_column
        if ["转发/元", "转发"].count(name) == 1:
            sheet.forward_price_index = cur_column
        if ["直发/元", "直发"].count(name) == 1:
            sheet.direct_send_price_index = cur_column
        if ["推荐级别"].count(name) == 1:
            sheet.recommend_level_index = cur_column
        if ["状态"].count(name) == 1:
            sheet.status_index = cur_column
        if ["状态码"].count(name) == 1:
            sheet.status_code_index = cur_column
        cur_column += 1

    return sheet


# 生成excel表格，默认取前7天的数据
def write_excel_file(weibo_data, sheet_name, workbook):
    now = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d'), "%Y-%m-%d")
    if weibo_data is not None and len(weibo_data) > 0:
        ws = workbook.add_sheet(sheet_name)
        ws.row(1).write(0, unicode('序号', 'utf-8'))
        ws.row(1).write(1, unicode('博主', 'utf-8'))
        ws.row(1).write(2, unicode('链接', 'utf-8'))
        ws.row(1).write(3, unicode('粉丝数/万', 'utf-8'))
        ws.row(1).write(4, unicode('平均转发数', 'utf-8'))
        ws.row(1).write(5, unicode('状态', 'utf-8'))
        ws.row(1).write(6, unicode('状态码', 'utf-8'))
        ws.col(0).width = 2222
        ws.col(1).width = 6666
        ws.col(2).width = 9999
        ws.col(3).width = 2222
        ws.col(4).width = 3000
        ws.col(5).width = 4444
        ws.col(6).width = 2222
        for index, item in enumerate(weibo_data):
            weibo_num = 0
            weibo_sum = 0

            if item.per_zhuanfa_num > 0:
                weibo_num = 1
                weibo_sum = item.per_zhuanfa_num
            else:
                for weibo in item.latest_weibo:
                    tmp_date = datetime.datetime.strptime(weibo.send_date.strftime('%Y-%m-%d'), "%Y-%m-%d")
                    if 0 < (now - tmp_date).days <= 7 and weibo.zhuanfa_num >= 10:
                        weibo_num += 1
                        weibo_sum += weibo.zhuanfa_num

            ws.row(2 + index).write(0, 1 + index)

            if item.bozhu_excel_name.strip() != "":
                ws.row(2 + index).write(1, unicode(item.bozhu_excel_name, 'utf-8'))

            if item.home_url.strip() != "":
                ws.row(2 + index).write(2, unicode(item.home_url, 'utf-8'))

            ws.row(2 + index).write(3, item.fensi_num if item.per_zhuanfa_num > 0 else int(
                round((item.fensi_num * 1.0) / 10000)))

            if weibo_num != 0:
                ws.row(2 + index).write(4, weibo_sum / weibo_num)
            else:
                ws.row(2 + index).write(4, 0)

            if item.data_status == MicroBlogModel.MicroBlogHome.DATA_STATUS_OK and weibo_sum > 0:
                ws.row(2 + index).write(5, unicode('正常', 'utf-8'))
                ws.row(2 + index).write(6, item.data_status)
            elif item.data_status == MicroBlogModel.MicroBlogHome.DATA_STATUS_URL_ERROR:
                ws.row(2 + index).write(5, unicode('链接错误', 'utf-8'))
                ws.row(2 + index).write(6, item.data_status)
            elif item.data_status == MicroBlogModel.MicroBlogHome.DATA_STATUS_ERROR:
                ws.row(2 + index).write(5, unicode('错误', 'utf-8'))
                ws.row(2 + index).write(6, item.data_status)
            else:
                ws.row(2 + index).write(5, unicode('数据错误', 'utf-8'))
                ws.row(2 + index).write(6, MicroBlogModel.MicroBlogHome.DATA_STATUS_ERROR)

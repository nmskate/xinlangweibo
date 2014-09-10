#!/usr/bin/env python
#coding=utf-8

import datetime
import xlrd
from model.exceldata import Excel, SheetItem, ExcelItem

'''允许的列名'''
ALLOW_COLUMNS = ["序号", "类型", "博主", "账号名称", "链接", "粉丝数/万", "粉丝/万", "平均转发数", "说明", "转发/元", "转发", "直发/元", "直发", "推荐级别"]

'''检查输入文件格式是否正确, 正确返回文件, 错误退出. 参数中的excel是exceldata.Excel类型'''
def __check_input_file(excel):
	flag = True
	excel.workbook = xlrd.open_workbook(excel.name)
	for sheet in excel.workbook.sheets():
		for name in sheet.row_values(1):
			if ALLOW_COLUMNS.count(name.encode('utf-8').replace(' ', '')) == 0:
				flag = False
				print "包含有不合法的列名 --- sheet名(", sheet.name, "), 列名(", name.encode('utf-8'), ")"
				print '''仅允许的列名 --- 序号, 类型, 博主, 账号名称, 链接, 粉丝数/万, 粉丝/万, 平均转发数, 说明, 转发/元, 转发, 直发/元, 直发, 推荐级别'''
	if not flag:
		sys.exit(1)
	else:
		return excel

'''获取excel, 并解析出excel中的数据, 返回exceldata.Excel类型'''
def read_excel_file(input_file_name):
	excel = __check_input_file(Excel(input_file_name))

	cur_sheet_index = 0
	for sheet in excel.workbook.sheets():
		sheet_item = SheetItem(cur_sheet_index, sheet.name)

		cur_index = 0
		for name in sheet.row_values(1):
			if ["序号"].count(name.encode('utf-8').replace(' ', '')) == 1:
				sheet_item.num_index = cur_index
			if ["博主", "账号名称"].count(name.encode('utf-8').replace(' ', '')) == 1:
				sheet_item.bozhu_name_index = cur_index
			if ["链接"].count(name.encode('utf-8').replace(' ', '')) == 1:
				sheet_item.link_index = cur_index
			if ["粉丝数/万", "粉丝/万"].count(name.encode('utf-8').replace(' ', '')) == 1:
				sheet_item.fensi_num_index = cur_index
			if ["平均转发数"].count(name.encode('utf-8').replace(' ', '')) == 1:
				sheet_item.per_zhuanfa_index = cur_index
			if ["说明"].count(name.encode('utf-8').replace(' ', '')) == 1:
				sheet_item.explain_index = cur_index
			if ["转发/元", "转发"].count(name.encode('utf-8').replace(' ', '')) == 1:
				sheet_item.zhuanfa_index = cur_index
			if ["直发/元", "直发"].count(name.encode('utf-8').replace(' ', '')) == 1:
				sheet_item.zhifa_index = cur_index
			cur_index += 1

		for index in range(sheet.nrows):
			excel_data_item = ExcelItem()
			if index >= 2 and sheet.cell(index, sheet_item.num_index).value != '':
				num = str(sheet.cell(index, sheet_item.num_index).value).encode('utf-8').strip()
				bozhu_name = sheet.cell(index, sheet_item.bozhu_name_index).value.encode('utf-8').strip()
				link = sheet.cell(index, sheet_item.link_index).value.encode('utf-8').strip()

				try:
					fensi_num = str(sheet.cell(index, sheet_item.fensi_num_index).value).encode('utf-8').strip()
					fensi_num = fensi_num[0 : len(fensi_num) - 1] if fensi_num != "" and fensi_num.endswith('W') else fensi_num
					fensi_num = fensi_num[0 : len(fensi_num) - 1] if fensi_num != "" and fensi_num.endswith('w') else fensi_num
				except:
					fensi_num = sheet.cell(index, sheet_item.fensi_num_index).value.encode('utf-8').strip()
					fensi_num = fensi_num[0 : fensi_num.find('万')] if fensi_num != "" and fensi_num.endswith('万') else fensi_num
				fensi_num = 0 if fensi_num == '' else fensi_num

				explain = sheet.cell(index, sheet_item.explain_index).value.encode('utf-8').strip()
				try:
					zhuanfa = str(sheet.cell(index, sheet_item.zhuanfa_index).value).encode('utf-8').strip()
				except:
					zhuanfa = '-1'
				try:
					zhifa = str(sheet.cell(index, sheet_item.zhifa_index).value).encode('utf-8').strip()
				except:
					zhifa = '-1'

				excel_data_item.num = int(float(num)) if num != "" else 0
				excel_data_item.bozhu_excel_name = bozhu_name
				excel_data_item.bozhu_name = bozhu_name[0 : len(bozhu_name) - 1] if bozhu_name != "" and bozhu_name.endswith('V') else bozhu_name
				excel_data_item.link = link
				excel_data_item.fensi_num = round(float("%.2f" % float(fensi_num)), 1)
				excel_data_item.explain = explain
				excel_data_item.zhuanfa = int(float(zhuanfa)) if zhuanfa != "" else 0
				excel_data_item.zhifa = int(float(zhifa)) if zhifa != "" else 0

				sheet_item.data_items.append(excel_data_item)

		excel.sheet_items.append(sheet_item)
		cur_sheet_index += 1
	return excel

'''生成excel表格，默认取前4天的数据'''
def output_weibo_data(weibo_data, excel_sheet, workbook):
	now = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d'), "%Y-%m-%d")
	if weibo_data is not None and len(weibo_data) > 0:
		ws = workbook.add_sheet(excel_sheet.name)
		ws.row(0).write(0, unicode('序号', 'utf-8'))
		ws.row(0).write(1, unicode('博主', 'utf-8'))
		ws.row(0).write(2, unicode('链接', 'utf-8'))
		ws.row(0).write(3, unicode('粉丝数/万', 'utf-8'))
		ws.row(0).write(4, unicode('平均转发数', 'utf-8'))
		for index, item in enumerate(weibo_data):
			weibo_num = 0
			weibo_sum = 0
			for weibo in item.latest_weibo:
				tmp_date = datetime.datetime.strptime(weibo.send_date.strftime('%Y-%m-%d'), "%Y-%m-%d")
				if ((now - tmp_date).days > 0 and (now - tmp_date).days <= 4):
					weibo_num += 1
					weibo_sum += weibo.zhuanfa_num

			ws.row(1 + index).write(0, 1 + index)

			if item.name.strip() != "":
				ws.row(1 + index).write(1, unicode(item.name, 'utf-8'))

			if item.home_url.strip() != "":
				ws.row(1 + index).write(2, unicode(item.home_url, 'utf-8'))

			ws.row(1 + index).write(3, int(round((item.fensi_num * 1.0) / 10000)))

			if weibo_num != 0:
				ws.row(1 + index).write(4, weibo_sum / weibo_num)
			else:
				ws.row(1 + index).write(4, 0)

			workbook.save('result_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.xlsx')
#!/usr/bin/env python
#coding=utf-8

import datetime
import xlrd

'''允许的列名'''
ALLOW_COLUMNS = ["序号", "类型", "博主", "账号名称", "链接", "粉丝数/万", "粉丝/万", "平均转发数", "说明", "转发/元", "转发", "直发/元", "直发", "推荐级别"]

'''检查输入文件格式是否正确, 正确返回文件, 错误退出'''
def __check_input_file(file_name):
	flag = True
	_file = xlrd.open_workbook(file_name)
	for sheet in _file.sheets():
		for name in sheet.row_values(1):
			if ALLOW_COLUMNS.count(name.encode('utf-8').replace(' ', '')) == 0:
				flag = False
				print "包含有不合法的列名 --- sheet名(", sheet.name, "), 列名(", name.encode('utf-8'), ")"
				print '''仅允许的列名 --- 序号, 类型, 博主, 账号名称, 链接, 粉丝数/万, 粉丝/万, 平均转发数, 说明, 转发/元, 转发, 直发/元, 直发, 推荐级别'''
	if not flag:
		sys.exit(1)
	else:
		return _file

'''获取excel文件'''
def get_excel_file(input_file_name):
	excel_sheets = {}
	return __check_input_file(input_file_name)

'''读取excel表格中的数据, 生成字典如{xxx : [xxx, xxx, xxx], xxx : [xxx, xxx, xxx]}, 字典对应的键是sheet的名,值是每个sheet的博主名, 并且是从第3行开始的博主名'''
def get_sheets_dict_from_file(excel_file):
	excel_sheets = {}
	for sheet in excel_file.sheets():
		bozhu_index = 0
		for name in sheet.row_values(1):
			if ["博主", "账号名称"].count(name.encode('utf-8').replace(' ', '')) == 1:
				break
			else:
				bozhu_index += 1

		bozhu_array = []
		for index in range(sheet.nrows):
			if index >= 2 and sheet.cell(index, bozhu_index).value.encode('utf-8').strip() != "":
				bozhu_name = sheet.cell(index, bozhu_index).value.encode('utf-8').strip()
				if bozhu_name.endswith('V'):
					bozhu_name = bozhu_name[0 : len(bozhu_name) - 1]
				bozhu_array.append(bozhu_name)

		excel_sheets[sheet.name.encode('utf-8')] = bozhu_array
	return excel_sheets

'''生成excel表格，默认取前4天的数据'''
def output_weibo_data(weibo_data, excel_sheel, workbook):
	now = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d'), "%Y-%m-%d")
	if weibo_data is not None and len(weibo_data) > 0:
		ws = workbook.add_sheet(excel_sheel.name)
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
			ws.row(1 + index).write(0, unicode(str(1 + index), 'utf-8'))
			ws.row(1 + index).write(1, unicode(item.name, 'utf-8'))
			ws.row(1 + index).write(2, unicode(item.home_url, 'utf-8'))
			ws.row(1 + index).write(3, unicode(str(int(round((item.fensi_num * 1.0) / 10000))), 'utf-8'))
			ws.row(1 + index).write(4, unicode(str(weibo_sum / weibo_num), 'utf-8'))
			workbook.save('result.xlsx')

#!/usr/bin/env python
#coding=utf-8

import datetime

'''生成excel表格，默认取前3天的数据'''
def create_output_file(weibo_data):
	now = datetime.datetime.now()

	if weibo_data is not None and len(weibo_data) > 0:
		for item in range(len(weibo_data)):
			print item.name, item.home_url, item.guanzhu_num, item.fensi_num, item.weibo_num

			for weibo in item.latest_weibo:
				if ((now - weibo.send_date).days <= 3):
					print weibo.send_date, weibo.zan_num ,weibo.zhuanfa_num, weibo.pinglun_num
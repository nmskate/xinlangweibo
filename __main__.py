#!/usr/bin/env python
#coding=utf-8

import weibo

if __name__ == "__main__":
    #抓取数据
    weibo_all_data = weibo.Weibo.fetch_weibo(['英国报姐'])
    #生成excel表格，只取前3天的数据
    excel.create_output_file(weibo_all_data)

    # for item in weibo_all_data:
    #     print item.name, item.home_url, item.guanzhu_num, item.weibo_num, item.fensi_num
    #     for item_data in item.latest_weibo:
    #         print item_data.send_date, item_data.zan_num, item_data.zhuanfa_num, item_data.pinglun_num

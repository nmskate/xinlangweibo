#!/usr/bin/env python
#coding=utf-8

import weibo

if __name__ == "__main__":
    weibo_all_data = weibo.Weibo.do_weibo(['英国报姐'])

    for item in weibo_all_data:
        print item.name, item.home_url, item.weibo_num, item.fensi_num, item.guanzhu_num
        for item_data in item.latest_weibo:
            print item_data.send_date, item_data.zan_num, item_data.zhuanfa_num, item_data.pinglun_num

#!/usr/bin/env python
#coding=utf-8

import os
import config
import crawl

if __name__ == "__main__":
    url = config.BASE_URL + '/uktimes'
    html = os.popen("http -b '" + url + "' User_Agent:'" + config.USER_AGENT + "' Cookie:'" + config.COOKIE + "'").read()

    start = html.find('pftb_itm S_line1')
    end = html.find('微博', start)
    tmp = html[(start + 1) : end]
    for i in range(1000):
        start = tmp.find('pftb_itm S_line1')
        if start == -1:
            href = tmp[tmp.find('href') : end]
            href = href[href.find('=') : href.find(' ')]
            print config.BASE_URL + href.replace("\\", '').strip("=\"")
            break
        else:
            tmp = tmp[(start + 1) : end]

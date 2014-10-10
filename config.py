#!/usr/bin/env python
#coding=utf-8

#新浪微博域
BASE_URL = '''http://weibo.com'''

#模拟浏览器, 默认浏览器:firefox 31.0, 操作系统: Ubuntu x86_64
USER_AGENT = '''Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0'''

#请求时所带的cookie
COOKIE = '''UOR=code.csdn.net,widget.weibo.com,www.doc88.com; SINAGLOBAL=543264989710.8888.1409128309644; ULV=1410856099295:28:22:3:4939517541865.38.1410856099209:1410761967533; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5s9DW1VreO60fXWlb.XQu-5JpX5KMt; myuid=1671687854; ALF=1442372466; wvr=5; TC-V5-G0=666db167df2946fecd1ccee47498a93b; SUS=SID-1671687854-1410836466-XD-oeygn-926cb607d3a51f0dd698c249a7feb693; SUE=es%3D67c9a881aec2cce75751f8ed62b2c69e%26ev%3Dv1%26es2%3D0e777fa208ed9a8736f7bf6f89ac8783%26rs0%3DYCJxtIJws6NLFrEYgU1XqRMUk76V1HILCCYz%252By%252FWtDSF5vMkjxM%252Ftphk6V16eaLwwaeGSbnE6Z9HCYl1ROpMh6DSHkUpq1FSlQoiftiOp3B8yyAKpSb4aAK0wCy8qKUn3L8RXS404Xto2YWx2Wy2Wu1JNNtXdjNeNuhQm0n86Lc%253D%26rv%3D0; SUP=cv%3D1%26bt%3D1410836466%26et%3D1410922866%26d%3Dc909%26i%3Db693%26us%3D1%26vf%3D0%26vt%3D0%26ac%3D0%26st%3D0%26uid%3D1671687854%26name%3Dnmjungyumi%2540sina.com%26nick%3D%25E7%2594%25A8%25E6%2588%25B71671687854%26fmp%3D%26lcp%3D; SUB=_2AkMjSyjFa8NlrAJXn_kTxGzqaYlH-jyQk6wzAn7uJhIyGxh-7gczqSXAaFqigEI-7rfRRkAXTBKQlzzl2A..; SSOLoginState=1410836466; TC-Ugrow-G0=5eac345e6f37d928953d6a363df28df7; _s_tentry=-; TC-Page-G0=9183dd4bc08eff0c7e422b0d2f4eeaec; Apache=4939517541865.38.1410856099209'''

#新浪微博按名字搜索的基础地址
BASE_URL_NAME_SEARCH = '''http://s.weibo.com/user/'''

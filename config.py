#!/usr/bin/env python
#coding=utf-8

'''新浪微博域'''
BASE_URL = "http://weibo.com"

'''模拟浏览器, 默认浏览器:firefox 31.0, 操作系统: Ubuntu x86_64'''
USER_AGENT = '''Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0'''

'''请求时所带的cookie'''
COOKIE = '''UOR=code.csdn.net,widget.weibo.com,login.sina.com.cn; SINAGLOBAL=543264989710.8888.1409128309644; ULV=1409561090516:8:2:2:4227622928624.788.1409561090502:1409542627959; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5s9DW1VreO60fXWlb.XQu-5JpX5K2t; un=nmjungyumi@sina.com; TC-Ugrow-G0=370f21725a3b0b57d0baaf8dd6f16a18; SUB=_2AkMjWP9Da8NlrAJXn_kTxGzqaYlH-jyQjvW1An7uJhIyHRh-7nIMqSUw5qi7AMKTZpb3uFHnQfXYBfTGZg..; TC-V5-G0=2bdac3b437dd23e235b79a3d6922ea06; _s_tentry=login.sina.com.cn; Apache=4227622928624.788.1409561090502; TC-Page-G0=4c4b51307dd4a2e262171871fe64f295; WBStore=4dccd3503335dcf9|undefined; myuid=1671687854; login_sid_t=361d5c48f7aa6c4fa5271840c5d977d8; WBtopGlobal_register_version=93e801de8661660d; SUS=SID-1671687854-1409577076-XD-13thf-b8dfe92432e8b450b0ceef274762b48a; SUE=es%3D464c9d0fd92fe10c9dc8b6bad9dff9e0%26ev%3Dv1%26es2%3De5710bfa36ab1ad0f65a43494ce8a0d1%26rs0%3DSF4Iyua3bVFNGXMay2Z%252FBk7PDbtx0sztGftbNvLMfhkgmaf7vyPcdSPbf1DEznNQ4qXaWP%252FF%252BRUEb%252BPuKW3aQaKs%252FK%252FlYSbCteLjeCO%252FZk7h2DzEIhfG62G9X%252BpYVVm6o7V7Zfg2dCR3LNyDZSiCGbh5VZ7YsJAJUlv8l1BBpdE%253D%26rv%3D0; SUP=cv%3D1%26bt%3D1409577076%26et%3D1409663476%26d%3Dc909%26i%3Db48a%26us%3D1%26vf%3D0%26vt%3D0%26ac%3D2%26st%3D0%26uid%3D1671687854%26name%3Dnmjungyumi%2540sina.com%26nick%3D%25E7%2594%25A8%25E6%2588%25B71671687854%26fmp%3D%26lcp%3D; ALF=1441113076; SSOLoginState=1409577076'''

'''新浪微博按名字搜索的基础地址'''
BASE_URL_NAME_SEARCH = "http://s.weibo.com/weibo/"

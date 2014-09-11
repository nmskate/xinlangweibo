#!/usr/bin/env python
#coding=utf-8

'''新浪微博域'''
BASE_URL = '''http://weibo.com'''

'''模拟浏览器, 默认浏览器:firefox 31.0, 操作系统: Ubuntu x86_64'''
USER_AGENT = '''Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0'''

'''请求时所带的cookie'''
COOKIE = '''UOR=code.csdn.net,widget.weibo.com,www.baidu.com; SINAGLOBAL=543264989710.8888.1409128309644; ULV=1410436603747:24:18:6:2912066781415.663.1410436603734:1410405669527; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5s9DW1VreO60fXWlb.XQu-5JpX5KMt; un=nmjungyumi@sina.com; myuid=1671687854; ALF=1441944775; TC-V5-G0=10672b10b3abf31f7349754fca5d2248; _s_tentry=news.ifeng.com; SUS=SID-1671687854-1410432145-XD-j9gno-2cfbd69898470da2c64168a2a9dcb693; SUE=es%3D3dac10ac15e6cbb75d82b2a402bec0dd%26ev%3Dv1%26es2%3D813b096019b143d7cbc3fc51de3d5d8b%26rs0%3DXnWnknw5NPgL2fqszlfLNDQwaPjz0sZe1MSLvE4N3UivPYrbhw%252FugWDY6hjhbYk6DQ95eupxaxDOFwtcMeq6tny2v0fEU6UmC0tpws9TCyh19qsIUOgHq2romspbspMDAIDPXI4KzG3JsHFCn6DuK%252FbBETjDIeFX7oDnVF9NYR4%253D%26rv%3D0; SUP=cv%3D1%26bt%3D1410432145%26et%3D1410518545%26d%3Dc909%26i%3Df297%26us%3D1%26vf%3D%26vt%3D%26ac%3D%26st%3D0%26uid%3D1671687854%26name%3Dnmjungyumi%2540sina.com%26nick%3D%25E7%2594%25A8%25E6%2588%25B71671687854%26fmp%3D%26lcp%3D; SUB=_2AkMjTfOma8NlrAJXn_kTxGzqaYlH-jyQnflQAn7uJhIyGxh77m8VqSXEb7r3QCayKMSceVT5QdVgIXrhqQ..; SSOLoginState=1410432145; TC-Ugrow-G0=1ae767ccb34a580ffdaaa3a58eb208b8; TC-Page-G0=07e0932d682fda4e14f38fbcb20fac81; Apache=2912066781415.663.1410436603734; wvr=5'''

'''新浪微博按名字搜索的基础地址'''
BASE_URL_NAME_SEARCH = '''http://s.weibo.com/user/'''

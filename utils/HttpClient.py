#!/usr/bin/env python3
# coding=utf-8

__author__ = 'zero.liu'

import socket
import os
import urllib

from http import cookiejar


class HttpClient:
    # 默认超时时间
    __DEFAULT_TIMEOUT = 5

    __timeout = __DEFAULT_TIMEOUT

    __opener = None

    def __init__(self, timeout=None, user_agent=None, cookie=None, cookie_file=None):
        if timeout:
            self.__timeout = timeout

        # 设置超时时间
        socket.setdefaulttimeout(timeout)

        if cookie_file:
            if not os.path.exists(cookie_file):
                file_ = open(cookie_file, 'w')
                file_.close()
            cookie_jar_ = cookiejar.LWPCookieJar(cookie_file)
        else:
            cookie_jar_ = cookiejar.LWPCookieJar()

        cookie_processor_ = urllib.request.HTTPCookieProcessor(cookie_jar_)

        self.__opener = urllib.request.build_opener(cookie_processor_, urllib.request.HTTPHandler)

        urllib.request.install_opener(self.__opener)

        if user_agent is not None or cookie is not None:
            self.__add_headers(user_agent=user_agent, cookie=cookie)

    '''添加默认的headers'''
    def __add_headers(self, user_agent, cookie):
        self.__opener.added_headers = [
            ('User-Agent', user_agent),
            ('Cookie', cookie),
            ('Connection', 'keep-alive'),
            ('Cache-Control', 'no-cache'),
            ('Accept-Language:', 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3'),
            ('Accept-Encoding', 'gzip, deflate')
        ]

    '''HTTP GET 方法'''
    def get(self, url, params={}):
        if params:
            url += '?' + urllib.parse.urlencode(params)

        try:
            response = self.__opener.open(url)
        except urllib.error.HTTPError as e:
            print(e)
        else:
            return response.read()

    '''HTTP POST 方法'''
    def post(self, url, params={}):
        params = urllib.parse.urlencode(params)
        try:
            response = self.__opener.open(url, params)
        except urllib.error.HTTPError as e:
            print(e)
        else:
            return response.read()

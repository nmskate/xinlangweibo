#!/usr/bin/env python3
# coding=utf-8

__author__ = 'zero.liu'
__date__ = '14 - 10 - 27'

import socket
import os
import urllib
import logging

from http import cookiejar


class HttpClient:
    # 默认超时时间
    __DEFAULT_TIMEOUT = 5

    __timeout = __DEFAULT_TIMEOUT

    __cookie_file = None

    __cookie_jar = None

    __opener = None

    __init_http_client = False

    '''添加默认的headers'''
    @classmethod
    def __add_headers(cls, user_agent, cookie):
        headers_ = [
            ('Connection', 'keep-alive'),
            ('Cache-Control', 'no-cache'),
            ('Accept-Language:', 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3'),
            ('Accept-Encoding', 'gzip, deflate')
        ]

        if user_agent:
            headers_.append(('User-Agent', user_agent))

        if cookie:
            headers_.append(('Cookie', cookie))

        cls.__opener.added_headers = headers_

    @classmethod
    def create_http_client(cls, timeout=None, user_agent=None, cookie=None, cookie_file=None, init_cookie=None):
        logging.info('Starting to create http client...')

        if not cls.__init_http_client:
            if timeout:
                cls.__timeout = timeout

            # 设置超时时间
            socket.setdefaulttimeout(timeout)

            loaded_cookie_file_ = False
            if cookie_file:
                cls.__cookie_file = cookie_file

                if not os.path.exists(cookie_file):
                    cls.__cookie_jar = cookiejar.LWPCookieJar()
                else:
                    try:
                        cls.__cookie_jar = cookiejar.LWPCookieJar(cookie_file)
                        cls.__cookie_jar.load(ignore_discard=True, ignore_expires=True)
                        loaded_cookie_file_ = True
                    except cookiejar.LoadError:
                        loaded_cookie_file_ = False
                        logging.error('Loading cookies from cookie file error, cookie file:' + cookie_file)
            else:
                cls.__cookie_jar = cookiejar.LWPCookieJar()

            cookie_processor_ = urllib.request.HTTPCookieProcessor(cls.__cookie_jar)
            cls.__opener = urllib.request.build_opener(cookie_processor_, urllib.request.HTTPHandler)
            urllib.request.install_opener(cls.__opener)

            # 如果cookie_file不为None并且成功加载文件中的cookie，则直接使用
            if loaded_cookie_file_:
                logging.info('Loading cookies from cookie file success.')

            # 如果没有得到cookie并且设置了初始化cookie的函数，那么执行初始化cookie函数，强制传入cookie_file参数
            if not loaded_cookie_file_ and init_cookie:
                logging.info('Trying to init cookie.')
                init_cookie()
            else:
                logging.info('Skipping init cookie function.')

            if user_agent is not None or cookie is not None:
                logging.info('Adding HTTP header.')
                cls.__add_headers(user_agent=user_agent, cookie=cookie)

            cls.__init_http_client = True

    '''HTTP GET 方法'''
    @classmethod
    def get(cls, url, params={}):
        if params:
            url += '?' + urllib.parse.urlencode(params)
        try:
            response = cls.__opener.open(url)
        except urllib.error.HTTPError as e:
            logging.error(e)
            return ''
        else:
            return response.read()

    '''HTTP POST 方法'''
    @classmethod
    def post(cls, url, params={}):
        params = urllib.parse.urlencode(params)
        try:
            response = cls.__opener.open(url, params)
        except urllib.error.HTTPError as e:
            logging.error(e)
            return ''
        else:
            return response.read()

    '''将当前cookie保存到文件'''
    @classmethod
    def save_cookie_in_file(cls):
        if cls.__cookie_file is not None and cls.__cookie_jar is not None:
            cls.__cookie_jar.save(cls.__cookie_file, ignore_discard=True, ignore_expires=True)
            logging.info('Saving cookie in file success, cookie_file:' + cls.__cookie_file)

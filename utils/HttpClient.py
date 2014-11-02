#!/usr/bin/env python3
# coding=utf-8

__author__ = 'zero.liu'

import socket
import os
import urllib
import Configuration
import base64
import re
import json
import hashlib
import rsa
import binascii

from http import cookiejar
from utils import StringUtils


class HttpClient:
    # 默认超时时间
    __DEFAULT_TIMEOUT = 5

    __timeout = __DEFAULT_TIMEOUT

    __cookie_file = None

    __cookie_jar = None

    __opener = None

    def __init__(self, timeout=None, user_agent=None, cookie=None, cookie_file=None, init_cookie=None):
        if timeout:
            self.__timeout = timeout

        # 设置超时时间
        socket.setdefaulttimeout(timeout)

        loaded_cookie_file_ = False
        if cookie_file:
            self.__cookie_file = cookie_file

            if not os.path.exists(cookie_file):
                self.__cookie_jar = cookiejar.LWPCookieJar()
            else:
                try:
                    self.__cookie_jar = cookiejar.LWPCookieJar(cookie_file)
                    self.__cookie_jar.load(ignore_discard=True, ignore_expires=True)
                except cookiejar.LoadError:
                    loaded_cookie_file_ = False
                    print('Loading cookies error')
        else:
            self.__cookie_jar = cookiejar.LWPCookieJar()

        cookie_processor_ = urllib.request.HTTPCookieProcessor(self.__cookie_jar)
        self.__opener = urllib.request.build_opener(cookie_processor_, urllib.request.HTTPHandler)
        urllib.request.install_opener(self.__opener)

        # 如果cookie_file不为None并且成功加载文件中的cookie，则直接使用
        if loaded_cookie_file_:
            print('Loading cookies success')
            return

        # 如果没有得到cookie并且设置了初始化cookie的函数，那么执行初始化cookie函数，强制传入cookie_file参数
        if init_cookie:
            init_cookie()

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
    @classmethod
    def get(cls, url, params={}):
        print(id(cls))
        if params:
            url += '?' + urllib.parse.urlencode(params)

        try:
            response = cls.__opener.open(url)
        except urllib.error.HTTPError as e:
            print(e)
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
            print(e)
            return ''
        else:
            return response.read()

    '''将当前cookie保存到文件'''
    @classmethod
    def save_cookie_in_file(cls):
        if cls.__cookie_file is not None and cls.__cookie_jar is not None:
            cls.__cookie_jar.save(cls.__cookie_file, ignore_discard=True, ignore_expires=True)


PRE_LOGIN_URL = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=%s&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.11)'


def get_pre_login_status(username_):
    """
        Perform pre login action, get pre login status, including server time, nonce, rsa kv, etc.
    """
    pre_login_url_ = PRE_LOGIN_URL % get_user(username_)
    data_ = HttpClient.get(pre_login_url_).read()
    p_ = re.compile('\((.*)\)')
    json_data = p_.search(data_).group(1)
    data_ = json.loads(json_data)
    server_time_ = str(data_['servertime'])
    nonce_ = data_['nonce']
    rsa_kv_ = data_['rsakv']
    return server_time_, nonce_, rsa_kv_


def get_pwd_wsse(pwd, servertime, nonce):
    """
    Get wsse encrypted password
    """
    pwd1 = hashlib.sha1(pwd).hexdigest()
    pwd2 = hashlib.sha1(pwd1).hexdigest()
    pwd3_ = pwd2 + servertime + nonce
    pwd3 = hashlib.sha1(pwd3_).hexdigest()
    return pwd3


def get_pwd_rsa(pwd, servertime, nonce):
    """
    Get rsa2 encrypted password, using RSA module from https://pypi.python.org/pypi/rsa/3.1.1, documents can be accessed at
    http://stuvel.eu/files/python-rsa-doc/index.html
    """
    # n, n parameter of RSA public key, which is published by WEIBO.COM
    #hardcoded here but you can also find it from values return from prelogin status above
    weibo_rsa_n = 'EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443'
    #e, exponent parameter of RSA public key, WEIBO uses 0x10001, which is 65537 in Decimal
    weibo_rsa_e = 65537
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(pwd)
    #construct WEIBO RSA Publickey using n and e above, note that n is a hex string
    key = rsa.PublicKey(int(weibo_rsa_n, 16), weibo_rsa_e)
    #get encrypted password
    encropy_pwd = rsa.encrypt(message, key)
    #trun back encrypted password binaries to hex string
    return binascii.b2a_hex(encropy_pwd)


def get_user(username):
    username_ = urllib.parse.quote(username)
    username_ = StringUtils.convert_to_bytes(username_)
    username = base64.encodebytes(username_)[:-1]
    return username


def do_login():
    username_ = 'nmjungyumi@sina.com'
    pwd_ = 'nmjungyumi'
    """"
        Perform login action with use name, password and saving cookies.
        @param username_: login user name
        @param pwd_: login password
        @param cookie_file_: file name where to save cookies when login succeeded
    """
    # POST data per login weibo, these fields can be captured using httpfox extension in Firefox
    login_data = {
        'entry': 'weibo',
        'gateway': '1',
        'from': '',
        'savestate': '7',
        'userticket': '1',
        'pagerefer': '',
        'vsnf': '1',
        'su': '',
        'service': 'miniblog',
        'servertime': '',
        'nonce': '',
        'pwencode': 'rsa2',
        'rsakv': '',
        'sp': '',
        'encoding': 'UTF-8',
        'prelt': '45',
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
        'returntype': 'META'
    }
    login_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.11)'
    try:
        servertime, nonce, rsakv = get_pre_login_status(username_)
    except:
        return
    #Fill POST data
    print('starting to set login_data')
    login_data['servertime'] = servertime
    login_data['nonce'] = nonce
    login_data['su'] = get_user(username_)
    login_data['sp'] = get_pwd_rsa(pwd_, servertime, nonce)
    login_data['rsakv'] = rsakv

    text = HttpClient.get(login_url, urllib.urlencode(login_data))
    p = re.compile('location\.replace\(\'(.*?)\'\)')
    try:
        #Search login redirection URL
        login_url = p.search(text).group(1)
        data = HttpClient.get(login_url)
        #Verify login feedback, check whether result is TRUE
        patt_feedback = 'feedBackUrlCallBack\((.*)\)'
        p = re.compile(patt_feedback, re.MULTILINE)
        feedback = p.search(data).group(1)
        feedback_json = json.loads(feedback)
        if feedback_json['result']:
            HttpClient.save_cookie_in_file()
            return 1
        else:
            return 0
    except:
        return 0


def init_http_client():
    #初始化HttpClient，即全局urllib2
    HttpClient(user_agent=Configuration.USER_AGENT, cookie_file='cookie.bak', init_cookie=do_login)

if __name__ == '__main__':
    init_http_client()
    print(HttpClient.get('http://www.weibo.com/kaifulee'))
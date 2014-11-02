#!/usr/bin/env python3
# coding=utf-8

__author__ = 'zero.liu'
__date__ = 14 - 10 - 31

"""
    模拟新浪微博登陆
    参考:https://github.com/yoyzhou/weibo_login/blob/master/weibo_login.py
"""


import os
import urllib
import base64
import re
import hashlib
import json
import binascii
import Configuration
from utils import HttpClient


COOKIE_FILE = 'cookie.bak'

#PRE_LOGIN_URL = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&client=ssologin.js(v1.4.5)'
PRE_LOGIN_URL = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=%s&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.11)'


def get_pre_login_status(username_):
    """
        Perform pre login action, get pre login status, including server time, nonce, rsa kv, etc.
    """
    pre_login_url_ = PRE_LOGIN_URL % get_user(username_)
    data_ = urllib2.urlopen(pre_login_url_).read()
    p_ = re.compile('\((.*)\)')
    json_data = p_.search(data_).group(1)
    data_ = json.loads(json_data)
    server_time_ = str(data_['servertime'])
    nonce_ = data_['nonce']
    rsa_kv_ = data_['rsakv']
    return server_time_, nonce_, rsa_kv_


def login(username_, pwd_):
    """"
        Login with username, password and cookies.
        (1) If cookie file exists then try to load cookies;
        (2) If no cookies found then do login and create a cookie file
    """
    loaded_ = True
    http_client = HttpClient()
    # If cookie file exists then try to load cookies
    if os.path.exists(cookie_file_):
        try:
            cookie_jar_ = cookielib.LWPCookieJar(cookie_file_)
            cookie_jar_.load(ignore_discard=True, ignore_expires=True)
        except cookielib.LoadError:
            loaded_ = False
            print 'Loading cookies error'

        #install loaded cookies for urllib2
        if loaded_:
            cookie_support_ = urllib2.HTTPCookieProcessor(cookie_jar_)
            opener_ = urllib2.build_opener(cookie_support_, urllib2.HTTPHandler)
            urllib2.install_opener(opener_)
            print 'Loading cookies success'
            return 1
        else:
            return do_login(username_, pwd_, cookie_file_)
    else:
        #If no cookies found
        return do_login(username_, pwd_, cookie_file_)


def do_login(username_, pwd_, cookie_file_):
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
    cookie_jar2 = cookielib.LWPCookieJar()
    cookie_support2 = urllib2.HTTPCookieProcessor(cookie_jar2)
    opener2 = urllib2.build_opener(cookie_support2, urllib2.HTTPHandler)
    urllib2.install_opener(opener2)
    login_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.11)'
    try:
        servertime, nonce, rsakv = get_pre_login_status(username_)
    except:
        return
    #Fill POST data
    print 'starting to set login_data'
    login_data['servertime'] = servertime
    login_data['nonce'] = nonce
    login_data['su'] = get_user(username_)
    login_data['sp'] = get_pwd_rsa(pwd_, servertime, nonce)
    login_data['rsakv'] = rsakv
    login_data = urllib.urlencode(login_data)
    http_headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0'}
    req_login = urllib2.Request(
        url=login_url,
        data=login_data,
        headers=http_headers
    )
    result = urllib2.urlopen(req_login)
    text = result.read()
    p = re.compile('location\.replace\(\'(.*?)\'\)')
    try:
        #Search login redirection URL
        login_url = p.search(text).group(1)
        data = urllib2.urlopen(login_url).read()
        #Verify login feedback, check whether result is TRUE
        patt_feedback = 'feedBackUrlCallBack\((.*)\)'
        p = re.compile(patt_feedback, re.MULTILINE)
        feedback = p.search(data).group(1)
        feedback_json = json.loads(feedback)
        if feedback_json['result']:
            cookie_jar2.save(cookie_file_, ignore_discard=True, ignore_expires=True)
            return 1
        else:
            return 0
    except:
        return 0


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
    username_ = urllib.quote(username)
    username = base64.encodestring(username_)[:-1]
    return username


if __name__ == '__main__':
    username = 'nmjungyumi@sina.com'
    pwd = 'nmjungyumi'
    cookie_file = COOKIE_FILE
    if login(username, pwd, cookie_file):
        print 'Login WEIBO succeeded'
        # if you see the above message, then do whatever you want with urllib2, following is a example for fetch Kaifu's Weibo Home Page
        #Trying to fetch Kaifu Lee's Weibo home page
        kaifu_page = urllib2.urlopen('http://www.weibo.com/kaifulee').read()
        print kaifu_page
    else:
        print 'Login WEIBO failed'

#!/usr/bin/env python3
# coding=utf-8

__author__ = 'zero.liu'
__date__ = 14 - 10 - 31


"""
    模拟新浪微博登陆
    参考:https://github.com/yoyzhou/weibo_login/blob/master/weibo_login.py
"""

import urllib
import base64
import re
import hashlib
import json
import binascii
import rsa
import logging
import Configuration

from utils.HttpClient import HttpClient
from utils import StringUtils
from common import Charset


#PRE_LOGIN_URL = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&client=ssologin.js(v1.4.5)'
PRE_LOGIN_URL = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=%s&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.11)'


def get_pre_login_status(username_):
    """
        Perform pre login action, get pre login status, including server time, nonce, rsa kv, etc.
    """
    pre_login_url_ = PRE_LOGIN_URL % get_user(username_)
    data_ = StringUtils.convert_to_str(HttpClient.get(pre_login_url_))
    p_ = re.compile('\((.*)\)')
    json_data = p_.search(data_).group(1)
    data_ = json.loads(json_data)
    server_time_ = str(data_['servertime'])
    nonce_ = data_['nonce']
    rsa_kv_ = data_['rsakv']
    return server_time_, nonce_, rsa_kv_


def get_pwd_wsse(pwd_, server_time_, nonce_):
    """
        Get wsse encrypted password
    """
    pwd1_ = hashlib.sha1(pwd_).hexdigest()
    pwd2_ = hashlib.sha1(pwd1_).hexdigest()
    pwd3_ = pwd2_ + server_time_ + nonce_
    pwd3_ = hashlib.sha1(pwd3_).hexdigest()
    return pwd3_


def get_pwd_rsa(pwd_, server_time_, nonce_):
    """
        Get rsa2 encrypted password, using RSA module from https://pypi.python.org/pypi/rsa/3.1.1, documents can be accessed at
        http://stuvel.eu/files/python-rsa-doc/index.html
    """
    # n, n parameter of RSA public key, which is published by WEIBO.COM
    # hardcoded here but you can also find it from values return from prelogin status above
    weibo_rsa_n_ = 'EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443'
    # e, exponent parameter of RSA public key, WEIBO uses 0x10001, which is 65537 in Decimal
    weibo_rsa_e_ = 65537
    message_ = str(server_time_) + '\t' + str(nonce_) + '\n' + str(pwd_)
    message_ = StringUtils.convert_to_bytes(message_)
    #construct WEIBO RSA Publickey using n and e above, note that n is a hex string
    key_ = rsa.PublicKey(int(weibo_rsa_n_, 16), weibo_rsa_e_)
    #get encrypted password
    encrypt_pwd_ = rsa.encrypt(message_, key_)
    #trun back encrypted password binaries to hex string
    return binascii.b2a_hex(encrypt_pwd_)


def get_user(username_):
    username_ = urllib.parse.quote(username_)
    username_ = StringUtils.convert_to_bytes(username_)
    username_ = base64.encodebytes(username_)[:-1]
    return username_


def do_login():
    logging.info('Starting to login...')
    username_ = Configuration.UESRNAME
    pwd_ = Configuration.PASSWORD
    """"
        Perform login action with use name, password and saving cookies.
        @param username_: login user name
        @param pwd_: login password
        @param cookie_file_: file name where to save cookies when login succeeded
    """
    # POST data per login weibo, these fields can be captured using httpfox extension in Firefox
    login_data_ = {
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
    login_url_ = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.11)'
    try:
        server_time_, nonce_, rsakv_ = get_pre_login_status(username_)
    except Exception as e:
        logging.error(e)
        return
    # Fill POST data
    print('starting to set login_data')
    login_data_['servertime'] = server_time_
    login_data_['nonce'] = nonce_
    login_data_['su'] = get_user(username_)
    login_data_['sp'] = get_pwd_rsa(pwd_, server_time_, nonce_)
    login_data_['rsakv'] = rsakv_

    text_ = HttpClient.get(login_url_, login_data_)
    text_ = StringUtils.convert_to_str(text_, Charset.GBK)
    p_ = re.compile('location\.replace\(\'(.*?)\'\)')
    try:
        # Search login redirection URL
        login_url_ = p_.search(text_).group(1)
        data_ = HttpClient.get(login_url_)
        data_ = StringUtils.convert_to_str(data_, Charset.GBK)
        #Verify login feedback, check whether result is TRUE
        patt_feedback_ = 'feedBackUrlCallBack\((.*)\)'
        p_ = re.compile(patt_feedback_, re.MULTILINE)
        feedback_ = p_.search(data_).group(1)
        feedback_json_ = json.loads(feedback_)
        if feedback_json_['result']:
            HttpClient.save_cookie_in_file()
    except Exception as e:
        logging.error(e)
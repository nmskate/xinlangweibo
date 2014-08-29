#!/usr/bin/env python
#coding=utf8

import time
import config

class Login:

    #登录信息配置
    __CONFIG_FILE = "config.txt"

    #微博登陆页地址
    __LOGIN_PAGE_URL = "http://weibo.com/login.php"

    #登陆页邮箱xpath
    __LOGIN_EMAIL_XPATH = "/html/body/div[1]/div[2]/div[2]/div[2]/div/div[5]/div[1]/div/input"

    #登陆页密码xpath
    __LOGIN_PASSWD_XPATH = "/html/body/div[1]/div[2]/div[2]/div[2]/div/div[5]/div[2]/div/input"

    #登陆页登陆按钮xpath
    __LOGIN_SUBMIT_XPATH = "/html/body/div[1]/div[2]/div[2]/div[2]/div/div[5]/div[6]/div[1]/a"

    __email = ""
    __password = ""

    @classmethod
    def init(cls):
        conf_file = open(cls.__CONFIG_FILE, 'r')
        for line in conf_file.readlines():
            line = line.strip()
            if (line[0:1] == "#"):
                continue
            else:
                pro_value = line.split("=")
                if (pro_value[0] == "email"):
                    cls.__email = pro_value[1]
                elif (pro_value[0] == "password"):
                    cls.__password = pro_value[1]
        return cls

    @classmethod
    def login(cls, driver):
        driver.get(cls.__LOGIN_PAGE_URL)
        time.sleep(config.WAIT_TIME)
        try:
            driver.find_element_by_xpath(cls.__LOGIN_EMAIL_XPATH).send_keys(cls.__email)
            driver.find_element_by_xpath(cls.__LOGIN_PASSWD_XPATH).send_keys(cls.__password)
            driver.find_element_by_xpath(cls.__LOGIN_SUBMIT_XPATH).click()
        except Exception, e:
            print '登录失败'
            raise e

        time.sleep(config.WAIT_TIME)


if __name__ == "__main__":
    from selenium import webdriver
    driver = webdriver.Firefox()
    try:
        Login.init().login(driver)
    finally:
        driver.quit()

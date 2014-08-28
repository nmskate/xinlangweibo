#!/usr/bin/env python
#coding=utf8

from config import Config
from selenium import webdriver
import time

class Login:
    __CONFIG_FILE = "config.txt"

    __email = ""
    __password = ""

    def __init__(self):
        conf_file = open(self.__CONFIG_FILE, 'r')
        for line in conf_file.readlines():
            line = line.strip()
            if (line[0:1] == "#"):
                continue
            else:
                pro_value = line.split("=")
                if (pro_value[0] == "email"):
                    self.__email = pro_value[1]
                elif (pro_value[0] == "password"):
                    self.__password = pro_value[1]

    '''获取登陆cookie'''
    def getCookie(self):
        driver = webdriver.Firefox()
        driver.get(Config.LOGIN_PAGE_URL)
        time.sleep(10)

        login_a_ele = driver.find_element_by_xpath(Config.LOGIN_A_XPATH)
        print login_a_ele.find_element_by_tag_name("./a").get_attribute("href")
        time.sleep(Config.WAIT_TIME)

        # email_ele = driver.find_element_by_xpath(Config.LOGIN_EMAIL_XPATH)
        # password_ele = driver.find_element_by_xpath(Config.LOGIN_PASSWD_XPATH)
        # email_ele.send_keys(self.__email)
        # password_ele.send_keys(self.__password)
        # driver.find_element_by_xpath(Config.LOGIN_SUBMIT_XPATH).click()
        #
        # time.sleep(Config.WAIT_TIME)
        # login_cookies = driver.get_cookies()
        # print login_cookies
        driver.quit()

if __name__ == "__main__":
    Login().getCookie()

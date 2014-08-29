#!/usr/bin/env python
#coding=utf8

from selenium import webdriver
import time
import login
import weibo

if __name__ == "__main__":
    driver = webdriver.Firefox()
    try:
        login.Login.init().login(driver)
        weibo.search_data(driver, '英国报姐')
    finally:
        driver.quit()

#!/usr/bin/env python3
# coding=utf-8

__author__ = 'zero.liu'

import re

from common import Charset


# 去除字符串中的不可打印字符
def strip_blank(string):
    if type(string) != str:
        string = str(string)
    return re.sub(r'\s', '', string)


# 仅保留字符串中的非数字，如果字符串中无数字，取默认值default
def retain_digit(string, default='0'):
    if type(string) != str:
        string = str(string)
    string = re.sub(r'\D', '', string).strip()

    if string == '':
        return default
    else:
        return string


# 将字符串转换成浮点型，如果不能转换，返回default
def convert_to_float(string, default=0.0):
    try:
        result = float(string)
    except ValueError:
        result = default
    return result


# 将字符串转换成整型，如果不能转换，返回default
def convert_to_int(string, default=0.0):
    try:
        result = int(float(string))
    except ValueError:
        result = default
    return result


# 将字符串转换成bytes类型
def convert_to_bytes(string, encoding=Charset.DEFAULT):
    if string is not None and isinstance(string, str):
        try:
            return bytes(string, encoding=encoding)
        except UnicodeDecodeError as e:
            raise e

    return string


# 将字符串转换成bytes类型
def convert_to_str(string, encoding=Charset.DEFAULT):
    if string is not None and isinstance(string, bytes):
        try:
            return str(string, encoding=encoding)
        except UnicodeDecodeError as e:
            raise e

    return string


if __name__ == "__main__":
    print(retain_digit('300w'))
    print(retain_digit('300W'))
    print(retain_digit('五万'))
    print(strip_blank('abc d e'))

    print(convert_to_bytes('中文'))
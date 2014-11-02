#!/usr/bin/env python3
# coding=utf-8

__author__ = 'skate'
__date__ = 14 - 11 - 2


def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton
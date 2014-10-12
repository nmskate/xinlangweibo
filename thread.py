#!/usr/bin/env python3
# coding=utf-8

__author__ = 'zero.liu'

import threading


class MyThread(threading.Thread):
    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.func = func
        self.name = name
        self.args = args

    def run(self):
        self.func(*self.args)

    def loop(self):
        pass
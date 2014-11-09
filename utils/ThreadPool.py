#!/usr/bin/env python3
# coding=utf-8

__author__ = 'zero.liu'

import threading

from time import sleep
from queue import Queue


# 可改变大小的线程池类。创建一个线程池接受任务，传递给线程执行任务
class ThreadPool:
    def __init__(self, thread_num):
        self.__resizeLock = threading.Condition(threading.Lock())
        self.__taskLock = threading.Condition(threading.Lock())
        self.__threads = []
        self.__tasks = Queue()
        self.__isJoining = False

        # 为线程池中的线程分配id
        self.__thread_id = 0

        self.set_thread_count(thread_num)

    # 重置线程池大小的公有方法，需要持有重置锁，然后调用重置的私有方法
    def set_thread_count(self, new_thread_num):
        # 如果关闭了线程池就不能重置线程池大小
        if self.__isJoining:
            return False

        self.__resizeLock.acquire()
        try:
            self.__set_thread_count_no_lock(new_thread_num)
        finally:
            self.__resizeLock.release()
        return True

    # 重置线程池大小的私有方法，这里假定已经持有了重置锁
    def __set_thread_count_no_lock(self, new_thread_num):
        # 增加线程池的大小
        while new_thread_num > len(self.__threads):
            new_thread = ThreadPoolThread(self)
            self.__threads.append(new_thread)

        # 减小线程池大小
        while new_thread_num < len(self.__threads):
            self.__threads[0].go_away()
            del self.__threads[0]

    # 获取线程池大小
    def get_thread_count(self):
        self.__resizeLock.acquire()
        try:
            return len(self.__threads)
        finally:
            self.__resizeLock.release()

    # 向任务队列中添加一个任务，task必须是一个可调用的函数
    def add_task(self, task, args=None, callback_task_=None):
        if self.__isJoining:
            return False
        if not callable(task):
            return False

        self.__taskLock.acquire()
        try:
            self.__tasks.put((task, args, callback_task_))
            return True
        finally:
            self.__taskLock.release()

    # 获取任务队列中的下一个任务
    def next_task(self):
        self.__taskLock.acquire()
        try:
            if self.__tasks.empty():
                return None, None, None
            else:
                return self.__tasks.get()
        finally:
            self.__taskLock.release()

    # 为线程池中的线程分配id
    def gen_thread_id(self):
        self.__thread_id += 1
        return self.__thread_id

    # 启动所有线程
    def start_all(self):
        for _thread in self.__threads:
            _thread.start()

    # 清空任务队列，终止线程池中所有线程。可选允许任务和线程执行完
    def join_all(self, wait_for_task=True, wait_for_threads=True):
        # 标记线程池处于joining状态，阻止任务队列添加任务
        self.__isJoining = True

        # 等待任务结束
        if wait_for_task:
            while not self.__tasks.empty():
                sleep(.1)

        # 通知线程退出
        self.__resizeLock.acquire()
        try:
            self.__set_thread_count_no_lock(0)
            self.__isJoining = True

            # 等待线程执行完退出
            if wait_for_threads:
                for t in self.__threads:
                    t.join()
                    del t

            # 重置线程池
            self.__isJoining = False
        finally:
            self.__resizeLock.release()


# 线程池中的线程类
class ThreadPoolThread(threading.Thread):
    threadSleepTime = 0.1

    # 为线程分配一个线程池
    def __init__(self, thread_pool):
        threading.Thread.__init__(self)
        self.__pool = thread_pool
        self.__isDying = False
        self.__thread_id = thread_pool.gen_thread_id()

    # 在收到退出信号前，一直取任务、执行任务
    def run(self):
        while not self.__isDying:
            cmd, args, callback = self.__pool.next_task()
            # 如果没有任务，就短暂休息
            if cmd is None:
                sleep(ThreadPoolThread.threadSleepTime)
            elif callback is None:
                cmd(args)
            else:
                callback(cmd(args))

    # 线程退出
    def go_away(self):
        self.__isDying = True

if __name__ == "__main__":

    from random import randrange

    def sort_task(data):
        print("SortTask starting for ", data)
        numbers = list(range(data[0], data[1]))
        for a in numbers:
            rnd = randrange(0, len(numbers) - 1)
            a, numbers[rnd] = numbers[rnd], a
        print("SortTask sorting for ", data)
        numbers.sort()
        print("SortTask done for ", data)
        return "Sorter ", data

    def wait_task(data):
        print("WaitTask starting for ", data)
        print("WaitTask sleeping for %d seconds" % data)
        sleep(data)
        return "Waiter", data

    def callback_task(data):
        print("Callback called for", data)

    pool = ThreadPool(4)

    sleep(1)
    pool.add_task(sort_task, (1000, 100000), callback_task)
    # pool.add_task(wait_task, 5, callback_task)
    pool.add_task(sort_task, (200, 200000), callback_task)
    # pool.add_task(wait_task, 2, callback_task)
    pool.add_task(sort_task, (3, 30000), callback_task)
    # pool.add_task(wait_task, 7, callback_task)
    pool.add_task(sort_task, (4, 40000), callback_task)
    pool.add_task(sort_task, (7, 70000), callback_task)
    pool.add_task(sort_task, (88, 80000), callback_task)
    pool.add_task(sort_task, (222, 20000), callback_task)

    pool.start_all()
    pool.join_all()

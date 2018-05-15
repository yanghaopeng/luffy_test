#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/23 8:55
# @Author  : hyang
# @File    : my_logset.py
# @Software: PyCharm

import logging
import os
from conf import settings

# 日志格式
log_format = '[%(asctime)s - %(levelname)s - %(name)s - %(filename)s - %(lineno)d ] %(message)s '

def get_mylogger(name):
    """
    get log
    :param name:
    :return:
    """
    logger = logging.getLogger(name)
    logger.setLevel(settings.LOG_LEVEL)

    console_handler = logging.StreamHandler()
    # 文件绝对路径
    logfile_path = os.path.join(settings.BASE_DIR, 'log',settings.LOG_FILE)
    file_handler = logging.FileHandler(logfile_path)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    file_format = logging.Formatter(fmt=log_format)
    console_format = logging.Formatter(fmt=log_format, datefmt='%Y-%m-%d %H:%M:%S ')

    console_handler.setFormatter(console_format)
    file_handler.setFormatter(file_format)

    return logger

if __name__ == '__main__':
    log = get_mylogger('access')
    log.info('access')
    log.error('Error')
    #
    # log1 = get_mylogger('trans')
    # log1.info('trans')



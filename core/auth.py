#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/14 22:57
# @Author  : hyang
# @Site    :
# @File    : auth.py
# @Software: PyCharm

import json
import time
import os
from conf import settings
from log import my_logset
from functools import wraps


# logger = my_logset.get_mylogger('access')


def login_required(func):
    """
     登录认证装饰器
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(*args,**kwargs):
        # print(args[0].get('is_authenticated'))
        if args[0].get('is_authenticated'):
            print('execute %s'%func.__name__)
            res = func(*args, **kwargs)
        else:
            exit('user is not authenticated')
        return res

    return wrapper


def acc_login(user, pwd,logger):
    """
     用户登录
    :param log_obj:
    :return:
    """
    # 账号文件
    account_file = os.path.join(settings.BASE_DIR,'account','%s.json'%user)
    if os.path.isfile(account_file):
        user_fp = open(account_file,'r',encoding='utf-8')
        account_data = json.load(fp=user_fp)
        if account_data["password"] == pwd:
            exp_time_stamp = time.mktime(time.strptime(account_data["expire_date"],'%Y-%m-%d'))
            status = account_data['status']
            if time.time() > exp_time_stamp:
                msg = 'Account [%s] has expired,please contact the back to get a new card!' % user
                logger.error(msg)

            elif status != 0:
                msg = 'Account [%s] has frozen' % user
                logger.error(msg)

            else:
                logger.info('***********欢迎{}登录***********'.format(user))
                return account_data
        else:
            logger.error("Account ID or password is incorrect!")
    else:
        msg = "Account [%s] does not exist!" % user
        logger.error(msg)

def auth_acc(user_data,logger):
    """
     用户登录
    :return:
    """
    retry_count = 0
    if user_data['is_authenticated'] is not True:
        while retry_count < 3:
            user = input('input username: ').strip()
            pwd = input('input password: ').strip()

            acc_data = acc_login(user, pwd,logger)
            if acc_data:
                user_data['is_authenticated'] = True
                return acc_data

            retry_count +=1
        else:
            exit("account too many login attempts" )


if __name__ == '__main__':
    logger = my_logset.get_mylogger('access')
    user_data = {'is_authenticated':False}
    auth_acc(user_data,logger)


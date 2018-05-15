
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/14 23:55
# @Author  : hyang
# @Site    :
# @File    : main.py
# @Software: PyCharm

import os
import json
from core import auth
from core.auth import login_required
from conf import settings
from log import my_logset



user_data = {
    'user_id':None,
    'is_authenticated':False,
    'user':None
}

# transaction logger
trans_logger = my_logset.get_mylogger('transaction')
# access logger
access_logger = my_logset.get_mylogger('access')

@login_required
def account_info(user_data):
    """
       print acoount_info
       :param acc_data:
       :return:
       """
    curr_data = user_data['user']
    current_user = ''' 
       --------- USER INFO --------
       user_id:     {}
       Credit :     {}
       Balance:     {}
       expire_date: {}      
       ----------------------------------
       '''.format(curr_data['id'], curr_data['credit'], curr_data['balance'],curr_data['expire_date'])
    access_logger.info(current_user)

@login_required
def withdraw(user_data):
    """

     print current balance and let user do the withdraw action
    :param user_data:
    :return:
    """
    curr_data = user_data['user']
    back_flag = False
    while not back_flag:
        withdraw_amount = input("Input withdraw amount:").strip()
        if withdraw_amount.isdigit():
                old_bal = curr_data['balance']
                curr_data['balance'] = old_bal - float(withdraw_amount)*settings.TRANS_TYPE['withdraw']['interest']
                if curr_data['balance']:
                    msg = "New Balance:%s" % (curr_data['balance'])
                    trans_logger.info(msg)
                    save_data(curr_data)
        elif withdraw_amount == 'b':
            back_flag = True
        else:
            msg = "[%s] is not a valid amount, only accept integer!" % withdraw_amount
            trans_logger.error(msg)



@login_required
def transfer(user_data):
    """
     print current balance and let user do the transfer action
    :param user_data:
    :return:
    """
    curr_data = user_data['user']
    back_flag = False
    while not back_flag:
        transfer_amount = input("Input transfer amount:").strip()
        tesla_data = get_data('tesla')  # 得到转账人的信息
        if transfer_amount.isdigit():
            transfer_amount = float(transfer_amount)  # 转账金额转化float
            old_bal = curr_data['balance']
            new_tesla_bal = tesla_data['balance'] + transfer_amount  # 得到转账人的余额
            curr_data['balance'] = old_bal - float(transfer_amount) * settings.TRANS_TYPE['withdraw']['interest']
            tesla_data['balance'] = new_tesla_bal
            if curr_data['balance']:
                msg = "New Balance: %s new_tesla_bal: %s " % (curr_data['balance'], new_tesla_bal)
                trans_logger.info(msg)
                # 保存数据
                save_data(curr_data)
                save_data(tesla_data)
        elif transfer_amount == 'b':
            back_flag = True
        else:
            msg = "[%s] is not a valid amount, only accept integer!" % transfer_amount
            trans_logger.error(msg)


def logout(user_data):
    """
    user logout
    :param acc_data:
    :return:
    """
    msg = "%s logout" % user_data['user_id']
    user_data['is_authenticated']= False


def save_data(acc_data):
    """
     保存acc_data
    :param acc_data:
    :return:
    """
    file = os.path.join(settings.BASE_DIR,'account',acc_data['id']+'.json')
    user_fp = open(file,'w',encoding='utf-8')
    print('save_data: ',file, acc_data)
    json.dump(acc_data,user_fp,ensure_ascii=False)
    user_fp.close()

def get_data(user_id):
    """
     得到acc_data
    :param user_id:
    :return:
    """
    file = os.path.join(settings.BASE_DIR, 'account', user_id+'.json')
    user_fp = open(file, 'r', encoding='utf-8')
    acc_data = json.load(user_fp)
    user_fp.close()
    return acc_data

def interactive(acc_data):

    '''
    interact with user
    :return:
    '''
    menu = """
    ------- Bank ---------
    1.  账户信息(功能已实现)
    2.  取款(功能已实现)
    3.  转账(功能已实现)
    4.  用户退出(功能已实现)
    """
    menu_dic = {
        '1': account_info,
        '2': withdraw,
        '3': transfer,
        '4': logout,
    }
    exit_flag = False
    while not exit_flag:
        print(menu)
        user_option = input(">>:").strip()
        if user_option in menu_dic:
            # print('accdata', acc_data)
            # print(menu_dic[user_option], acc_data)
            menu_dic[user_option](acc_data)
        else:
            print("Option does not exist!", "error")
            exit_flag = True


def run():
    '''
    this function will be called right a way when the program started, here handles the user interaction stuff
    :return:
    '''
    acc_data = auth.auth_acc(user_data,access_logger)
    # print(acc_data)
    # 如果用户认证成功
    if user_data['is_authenticated']:
         user_data['user'] = acc_data
         user_data['user_id'] = acc_data.get('id')
         interactive(user_data)


if __name__ == '__main__':
    run()
    # print(a[0])
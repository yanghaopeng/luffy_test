import os

'''
日志文件设置
'''
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_LEVEL='INFO'
LOG_FILE='bank.log'

'''
交易类型
'''
TRANS_TYPE={
    'withdraw':{'interest':0.05,'action':'minus'},
    'transfer': {'interest': 0.05, 'action': 'minus'}
}

print(BASE_DIR)
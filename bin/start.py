import sys,os

BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)  # 加入环境变量

from core import main as m

if __name__ == '__main__':
    m.run()
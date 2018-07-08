import pickle
import os
from conf.setting import ADMIN_DB_PATH
from conf.setting import USER_DB_PATH
from conf.setting import LOG_PATH


def get_info(name, power):  # 拿到用户信息
    if power == 'admin':
        user_path = os.path.join(ADMIN_DB_PATH, '%s.pkl' % name)
    else:
        user_path = os.path.join(USER_DB_PATH, '%s.pkl' % name)
    if not os.path.exists(user_path):
        return
    with open(user_path, 'rb') as f:
        user_info = pickle.load(f)
        return user_info


def save_info(info):  # 存储用户信息
    if info['power'] == 'admin':
        user_path = os.path.join(ADMIN_DB_PATH, '%s.pkl' % info['name'])
    else:
        user_path = os.path.join(USER_DB_PATH, '%s.pkl' % info['name'])
    with open(user_path, 'wb') as f:
        pickle.dump(info, f)


def get_bill(user_info):
    user_log_path = os.path.join(LOG_PATH,user_info['name'])
    with open(user_log_path,'r',encoding='utf-8') as f:
        bill = f.read()
        return bill
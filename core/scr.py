from db import load_dump
from lib import common
from lib import make_diary

user_info = {}


def check_power(power='user'):  # 登录功能的装饰器
    def login_doc(func):
        def inner(*args, **kwargs):
            if user_info:
                res = func(*args, **kwargs)
                return res
            while True:
                user_name = input('请输入您的账号')
                per_info = load_dump.get_info(user_name, power)  # 读取文件数据
                if not per_info:
                    print('用户不存在')
                    continue
                if per_info['state'] == 1:
                    print('该账号已被冻结')
                    continue
                count = 0
                while count < 3:
                    password = input('请输入您的密码')
                    password_res = common.check_password(per_info, password)  # 验证密码
                    if not password_res:
                        print('密码错误')
                        count += 1
                        continue
                    user_info.update(per_info)  # 将拿到的信息更新到全局的字典
                    global per_logger, atm_logger
                    per_logger = make_diary.per_logger()
                    atm_logger = make_diary.atm_logger()
                    func_res = func(*args, **kwargs)
                    return func_res
                print('错误三次，账号冻结！')
                per_info['state'] = 1
                load_dump.save_info(per_info)  # 将修改后的的数据存到文件
                return False

        return inner

    return login_doc


@check_power()
def user_login():  # 用户登录
    if user_info:
        per_logger.info('%s登录了账号' % user_info['name'])
        return True


@check_power(power='admin')
def admin_login():  # 管理员登录
    if user_info:
        per_logger.info('%s登录了账号' % user_info['name'])
        return True


def register():  # 注册功能
    while True:
        user_name = input('请输入您的账号')
        res = load_dump.get_info(user_name, 'user')
        if res:
            print('注册失败，账户已存在')
            continue
        break
    while True:
        password1 = input('请输入您的密码')
        password2 = input('请确认密码')
        if password1 == password2:
            info = common.set_info(user_name, password1, 'user')
            load_dump.save_info(info)
            print('注册成功')
            return
        else:
            print('两次密码不一致')


def shopping():  # 购物
    shopping_car = {}
    product_list = [['Iphone7', 5800],
                    ['Coffee', 30],
                    ['疙瘩汤', 10],
                    ['Python Book', 99],
                    ['Bike', 199],
                    ['ViVo X9', 2499],
                    ]
    while True:
        for index, product in enumerate(product_list):
            print(index, product[0], product[1])
        choose = input('请输入与您想要购买的商品,b结账，q退出')
        if choose == 'b':
            total, info = common.check_out(user_info, shopping_car)  # 结账
            if not info:
                print('余额不足')
                continue
            load_dump.save_info(info)
            per_logger.info('%s购物花费%s元' % (user_info['name'], total))
            atm_logger.info('%s购物花费%s元' % (user_info['name'], total))
            print('购买成功')
            return
        if choose == 'q':
            print('放弃购买')
            return
        int_choose = common.check_digit(choose)
        if not int_choose and int_choose != 0:
            print('请输入整数或b结账，q退出')
            continue
        if int_choose >= len(product_list):
            print('商品超出范围')
            continue
        while True:
            count = input('请输入购买数量')
            int_count = common.check_digit(count)
            if not int_count:
                print('请输入整数')
                continue
            shopping_car = common.updata_shopping_car(product_list, shopping_car, int_choose, int_count)  # 更新购物车
            break


def withdraw():  # 提现
    while True:
        money = input('请输入您想要提现的金额')
        int_money = common.check_digit(money)
        if not int_money:
            print('请输入整数')
            continue
        take_off = int_money * 1.05
        info = common.check_balance(user_info, take_off)
        if not info:
            print('余额不足')
            continue
        load_dump.save_info(info)
        print('提现成功')
        per_logger.info('%s提现%s元' % (user_info['name'], int_money))
        atm_logger.info('%s提现%s元' % (user_info['name'], int_money))
        break


def transfer():  # 转账
    while True:
        money = input('请输入您想要转账的金额')
        int_money = common.check_digit(money)
        if not int_money:
            print('请输入整数')
            continue
        info = common.check_balance(user_info, int_money)
        if not info:
            print('余额不足')
            continue
        break
    while True:
        target = input('请输入目标账户')
        target_info = load_dump.get_info(target, 'user')
        if not target_info:
            print('账户不存在')
            continue
        target_info = common.add_money(target_info, int_money)
        load_dump.save_info(target_info)
        load_dump.save_info(info)
        print('转账成功')
        per_logger.info('%s转账给%s %s元' % (user_info['name'], target, int_money))
        atm_logger.info('%s转账给%s %s元' % (user_info['name'], target, int_money))
        break


def repay():  # 还款
    while True:
        should_repay = user_info['quota'] - user_info['balance']
        print('您还欠款%s元' % should_repay)
        money = input('请输入您想要还款的金额')
        int_money = common.check_digit(money)
        if not int_money:
            print('请输入整数')
            continue
        info = common.add_money(user_info, int_money)
        load_dump.save_info(info)
        print('还款成功')
        per_logger.info('%s还款%s元' % (user_info['name'], int_money))
        atm_logger.info('%s还款%s元' % (user_info['name'], int_money))
        break


def check_info():  # 查看个人信息
    print(user_info)
    bill = load_dump.get_bill(user_info)
    print(bill)


def add_admin():  # 添加管理员账户
    while True:
        user_name = input('请输入您的账号')
        res = load_dump.get_info(user_name, 'admin')
        if res:
            print('注册失败，账户已存在')
            continue
        break
    while True:
        password1 = input('请输入您的密码')
        password2 = input('请确认密码')
        if password1 == password2:
            info = common.set_info(user_name, password1, 'admin')
            load_dump.save_info(info)
            print('注册成功')
            per_logger.info('%s添加了管理员账户%s' % (user_info['name'], user_name))
            atm_logger.info('%s添加了管理员账户%s' % (user_info['name'], user_name))
            return
        else:
            print('两次密码不一致')


def quota():  # 提升额度
    while True:
        money = input('请输入想要提升的额度')
        int_money = common.check_digit(money)
        if not int_money:
            print('请输入整数')
            continue
        break
    while True:
        target = input('请输入需要提升额度的账户')
        info = load_dump.get_info(target, 'user')
        if not info:
            print('该账户不存在')
            continue
        info = common.add_quota(info, int_money)
        load_dump.save_info(info)
        print('提升额度成功')
        per_logger.info('%s为%s提升了%s额度' % (user_info['name'], target, int_money))
        atm_logger.info('%s为%s提升了%s额度' % (user_info['name'], target, int_money))
        break


def freezing_account():  # 冻结账号
    while True:
        target = input('请输入您想要冻结的账号')
        info = load_dump.get_info(target, 'user')
        if not info:
            print('该账户不存在')
            continue
        info['state'] = 1
        load_dump.save_info(info)
        print('冻结成功')
        per_logger.info('%s冻结了账户%s' % (user_info['name'], target))
        atm_logger.info('%s冻结了账户%s' % (user_info['name'], target))
        break


def thaw_account():  # 解冻账号
    while True:
        target = input('请输入您想要解冻的账号')
        info = load_dump.get_info(target, 'user')
        if not info:
            print('该账户不存在')
            continue
        info['state'] = 0
        load_dump.save_info(info)
        print('解冻成功')
        per_logger.info('%s解冻了账户%s' % (user_info['name'], target))
        atm_logger.info('%s解冻了账户%s' % (user_info['name'], target))
        break


def run():
    power_info1 = '''
    1.用户登录
    2.用户注册
    3.管理员登录
    4.退出
    '''
    power_info2 = {
        '1': user_login,
        '2': register,
        '3': admin_login,
        '4': quit
    }
    while True:
        print(power_info1)
        choose_login = input('请输入您的登入权限')
        if choose_login not in power_info2:
            print('请输入对应序号')
            continue
        res = power_info2[choose_login]()
        if not res:
            continue
        break
    while True:
        if user_info['power'] == 'admin':
            admin_info1 = '''
            1.添加管理员账户
            2.用户额度
            3.冻结账户
            4.解冻账户
            5.退出
            '''
            admin_info2 = {
                '1': add_admin,
                '2': quota,
                '3': freezing_account,
                '4': thaw_account,
                '5': quit
            }
            print(admin_info1)
            admin_choose = input('请输入您的需求')
            if admin_choose not in admin_info2:
                print('请输入对应序号')
                continue
            admin_info2[admin_choose]()
        else:
            if user_info['power'] == 'user':
                user_info1 = '''
                1.购物
                2.提现
                3.转账
                4.还款
                5.查询
                6.退出
                '''
                user_info2 = {
                    '1': shopping,
                    '2': withdraw,
                    '3': transfer,
                    '4': repay,
                    '5': check_info,
                    '6': quit
                }
                print(user_info1)
                user_choose = input('请输入您的需求')
                if user_choose not in user_info2:
                    print('请输入对应序号')
                    continue
                user_info2[user_choose]()

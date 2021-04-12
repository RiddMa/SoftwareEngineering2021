class Admin:
    def __init__(self, id, username, password, token):
        #数据库中的id
        self.id = id
        #管理员名字
        self.username = username
        #管理员登录密码
        self.password = password
        #生成的token（现在可以先不实现）
        self.token = token

    @staticmethod
    #跟据管理员名字查询对应信息，并对比密码设置error_code，
    # (token可先随意设置一个值，以后再改进)
    def get_admin(username, password):
        error_code = 0
        return error_code, Admin()

    # 生成报表，根据当前时间查询当前所有房间空调状态(开关、温度、风速等)与折扣
    @staticmethod
    def get_report(time):
        error_code = 0
        # 房间信息列表(空调状态与折扣)
        list = list()
        return error_code, list

    #这里我不太理解流水是啥，接口可能设置不正确
    @staticmethod
    def water_bills(time):
        error_code = 0
        return error_code, list()

    #设置某个房间的折扣
    @staticmethod
    def set_discount(rid, discount):
        error_code = 0
        return error_code

    # 设置所有空调总开关
    @staticmethod
    def center_turn_on_off(state):
        error_code = 0
        return error_code

# 房卡信息
class Card:
    def __init__(self, username, rid, password):
        # 顾客姓名
        self.useranme = username
        # 房间号
        self.rid = rid
        # 密码
        self.password = password

class Reception:
    # 根据预留电话号码返回一个房卡对象
    @staticmethod
    def get_card(phonenumber):
        error_code = 0
        return error_code, Card()

    # 退房结算
    @staticmethod
    def get_total_cost(rid):
        error_code = 0
        # 使用时间
        duration = 0
        # 消费金额
        price = 0.00
        return error_code, str(duration), str(price)


class User:

    # 顾客设置空调开关
    @staticmethod
    def turn_on_off(rid, state):
        error_code = 0
        return error_code

    # 顾客设置温度
    @staticmethod
    def set_temp(rid, temp):
        error_code = 0
        return error_code

    # 顾客设置风速
    @staticmethod
    def set_mode(rid, mode):
        error_code = 0
        return error_code

    # 顾客查看当前消费金额
    @staticmethod
    def show_cost(rid):
        error_code = 0
        # 空调开关状态
        onoff = 0
        cost = 0.00
        return error_code, str(onoff), str(cost);

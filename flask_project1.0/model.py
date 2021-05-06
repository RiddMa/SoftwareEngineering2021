import json
import time
import hashlib
import db
import math


class Ac:
    """
    用以描述空调的类
    __state：开启/关闭/待机(等待启动)状态
    __tempnow：当前温度
    __tempgoal：目标温度
    __mode：风速
    __lastsettletime：上次结算时间（单位：int
    __starttime：本次开机时间
    """
    TEMP_OUTSIDE = 12.9
    c = 0.01
    Q = 0.04
    __slots__ = ('__state', '__tempnow', '__tempgoal', '__mode', '__pattern', '__lastsettletime',
                 '__starttime',)

    def __init__(self, state, temp_now, temp_goal, mode, last_settle_time, pattern, start_time):
        self.__state = state
        self.__tempnow = temp_now
        self.__tempgoal = temp_goal
        self.__mode = mode
        self.__pattern = pattern
        self.__lastsettletime = last_settle_time
        self.__starttime = start_time

    @staticmethod
    def ac_temp_change(temp: float, passtime: int, pattern: int):
        """
        计算空调工作一段时间内温度变化的函数，仅和模式相关，不考虑设定温度
        令 c=ks = 0.01〖min〗^(-1) 其中k为介质温度传递系数，s为接触面积，
        T = T_平衡 + (〖T_平衡-T〗_初始) e ^ (-ct)
        T_平衡= T_外界+Q/c
        取　Q = +- 0.4
        T_外界 = 12.9 （北京年平均气温
        :param temp:原本的温度
        :param passtime:经过的时间
        :param pattern:制冷/制热模式对应0/1
        :return:空调运行状态下passtime之后的的温度
        """
        temp_balance = Ac.TEMP_OUTSIDE
        if pattern:
            temp_balance += Ac.Q / Ac.c
        else:
            temp_balance -= Ac.Q / Ac.c
        temp_new = temp_balance + (temp - temp_balance) * math.e ** (-passtime * Ac.c)
        return temp_new

    def natural_temp_change(self, temp: float, passtime: int):
        """
        计算一段时间内温度自然变化的函数
        :param temp:原本的温度
        :param passtime:经过的时间
        :return:自然状态下passtime时间之后的温度
        """
        temp_balance = Ac.TEMP_OUTSIDE
        temp_new = temp_balance + (temp - temp_balance) * math.e ** (-passtime * Ac.c)
        return temp_new

    def settle(self):
        """
        用来计算当前温度的函数
        :return: 当前温度
        """
        time_now = int(time.time())
        temp_after = self.__tempnow
        temp_previous = self.__tempnow
        if self.__state == 1:
            temp_after = self.ac_temp_change(temp_previous, time_now - self.__lastsettletime, self.__pattern)
            if self.__pattern == 0:
                temp_after = max(temp_after, self.__tempgoal)
            else:
                temp_after = min(temp_after, self.__tempgoal)
        else:
            temp_after = self.natural_temp_change(temp_previous, time_now - self.__lastsettletime)
        return temp_after

    def calccost(self):
        """
        更新花费金额到当前时间
        包括修改上次结算时间，更新当前温度
        :return:本次更新周期中的花费
        """
        prevtemp = self.__tempnow
        self.__tempnow = self.settle()
        timenow = int(time.time())
        self.__lastsettletime = timenow
        deltatemp = self.__tempnow - prevtemp
        if self.__state == 0:
            return 0
        if self.__mode == 'L':
            return 0.5 * deltatemp
        if self.__mode == 'M':
            return 1 * deltatemp
        if self.__mod == 'H':
            return 2 * deltatemp

    def changework(self, newtemp: float, newmode: str, newpattern: int):
        """
        修改空调工作模式
        :param newtemp:
        :return:
        """
        self.settle()
        if newtemp is not None:
            self.__tempgoal = newtemp
        if newmode is not None:
            self.__mode = newmode
        if newpattern is not None:
            self.__pattern = newpattern


class Room:
    '''
    房间类：
    __rid：房间号
    __state：开启/关闭/待机(等待启动)状态
    __tempnow：当前温度
    __tempgoal：目标温度
    __mode：风速
    __lastsettletime：上次结算时间（单位：int
    __cost：本次开机到现在的花销
    __totalduration：本次开机的总时长
    __last_start_time：本次开机时间
    __discount：本房间折扣
    '''
    __slots__ = ('__rid', '__ac', '__cost', '__discount')

    def __init__(self, rid, state, temp_now, temp_goal, mode, last, cost, discount, totaltime=0, starttime=0):
        self.__rid = rid
        self.__state = state
        self.__temp_now = temp_now
        self.__temp_goal = temp_goal
        self.__mode = mode
        self.__cost = cost
        self.__last_settle_time = last
        self.__total_duration = totaltime
        self.__last_start_time = starttime
        self.__discount = discount

    def settle(self):
        time_now = int(time.time())

    def set_temp(self, new_temp):
        self.__temp = new_temp
        return

    def changecost(self, deltcost):
        self.cost += deltcost
        return

    def changelasttime(self, newtime):
        self.totaltime += newtime - self.last
        self.last = newtime
        return

    def changediscount(self, discount):
        self.discount = discount
        return

    def setmode(self, newmode):
        newtime = int(time.time())
        self.changecost(self.Costcalc(newtime - self.last))
        self.changelasttime(newtime)
        self.mode = newmode
        return

    def Costcalc(self, time):
        switch = {'H': 0.03, 'M': 0.02, 'L': 0.01}
        res = switch[self.mode] * time / 60 * self.discount
        return res

    def updatecost(self):
        timenow = int(time.time())
        self.changecost(self.Costcalc(timenow - self.last))
        self.changelasttime(timenow)

    def Turnon(self):
        self.__state = 1
        self.cost = 0.5
        newtime = int(time.time())
        self.last = newtime
        self.starttime = newtime
        return

    def Turnoff(self):
        self.__state = 0
        newtime = int(time.time())
        self.changecost(self.Costcalc(newtime - self.last))
        self.changelasttime(newtime)
        db.addBill(self.rid, self.starttime, newtime, self.cost)
        return


class Roomlist:
    dict = dict()


roomlist = ['testOnly']
for j in range(1, 6):
    for i in range(1, 11):
        roomlist.append(str(j) + ('0' + str(i))[-2:])
roomstate = {i: 0 for i in roomlist}
Store = {i: Room(i, 0, 26, 'L', int(time.time()), 0, 1.0) for i in roomlist}


class Stuff:
    '''
    这是工作人员的类
    实例属性：用户名和密码
    类属性：token_pool,一个用来存储token和帐号对应用户名和类型
    方法：
    '''
    __slots__ = ('__username', '__password')
    token_pool = dict()

    def __init__(self, username: str, password: str):
        '''
        :param username:传入的工作人员用户名
        :param password:工作人员密码
        '''
        self.__username = username
        self.__password = password

    @staticmethod
    def login(self, username: str, password: str):
        '''
        用于登陆的方法，过程中需要校验用户名和密码
        :param username: 传入的工作人员用户名
        :param password: 工作人员密码
        :return: error_code、token和该工作人员的类型/权限
        '''
        error_code = 0
        return error_code

    @staticmethod
    def get_stuff_token(username: str, privilege):
        '''
        用于生成空调管理人员token的方法
        :param username:传入的工作人员用户名
        :return:token
        '''
        ctime = str(time.time())
        token = hashlib.md5(bytes(username, encoding="utf-8"))
        token.update(bytes(ctime, encoding="utf-8"))
        token = token.hexdigest()
        Stuff.token_pool[token] = (username, privilege)
        return token


class Ac_admin(Stuff):
    '''
    空调管理员的类
    包括一个查找所有给定房间状态的方法
        我很想写一颗trie树2333 —— 07
    '''

    @staticmethod
    def spy_on_ac(field: str):
        '''
        根据传入的字符串查找空调信息并返回，由于目前通信接口没定，先放着
        :param field: 传入字段(支持局部关键词查询
        :return: 返回一个list和error_code
        '''
        error_code = 0
        res = []
        return error_code, res

    # 跟据管理员名字查询对应信息，并对比密码设置error_code，
    # (token可先随意设置一个值，以后再改进)
    def get_admin(username, password):
        error_code = 0
        res = json.dumps(db.getUser(username, password).get_json())
        if 'userid' in res:
            return error_code, Ac_admin(res['userid'], username, password)
        else:
            error_code = 1
        return error_code, Ac_admin(0, None, None)

    # 生成报表，根据当前时间查询当前所有房间空调状态(开关、温度、风速等)与折扣
    @staticmethod
    def get_report(time):
        error_code = 0
        # 房间信息列表(空调状态与折扣)
        reslist = []
        for rid, value in Store.items():
            tpvar = dict()
            tpvar['rid'] = rid
            tpvar['__state'] = value.__state
            tpvar['temp'] = value.temp
            tpvar['mode'] = value.mode
            tpvar['discount'] = value.discount
            reslist.append(tpvar)
        return error_code, reslist

    # 这里我不太理解流水是啥，接口可能设置不正确
    # 应该是每天的实际入账金额，先空着
    @staticmethod
    def water_bills(time):
        error_code = 0
        starttime = float(time) // 60 // 24 * 60 * 24
        endtime = float(time) // 60 // 24 * 60 * 24 + 60 * 24
        res = db.getTurnover(int(starttime), int(endtime)).get_json()
        if 'msg' in res:
            error_code = 1
            return error_code, None
        return error_code, res

    # 设置某个房间的折扣
    @staticmethod
    def set_discount(rid, discount):
        error_code = 0
        if Store[rid].__state == 0:
            Store[rid].discount = discount
            return error_code
        Store[rid].updatecost()
        Store[rid].changediscount(discount)
        return error_code

    # 设置所有空调总开关
    @staticmethod
    def center_turn_on_off(state):
        error_code = 0
        for i in roomlist:
            if Store[i].__state != state:
                if state == 1:
                    Store[i].Turnon()
                else:
                    Store[i].Turnoff()
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


class Receptionist(Stuff):
    '''
        前台接待人员的类
        包括入住、退房、打报表的方法
    '''

    @staticmethod
    def get_card(phonenumber):
        error_code = 0
        res = db.getInfomation(phonenumber).get_json()
        if 'msg' in res:
            error_code = 1
            return error_code, None
        return error_code, Card(res['name'], Card['roomid'], Card['password'])

    # 退房结算
    @staticmethod
    def get_total_cost(rid):
        error_code = 0
        if Store[rid].__state == 1:
            Store[rid].Turnoff()
        # 使用时间
        duration = Store[rid].totaltime
        # 消费金额
        price = Store[rid].cost
        return error_code, int(duration), float(price)


class User:
    def __init__(self, uid, username, token='x'):
        self.id = uid
        self.name = username
        self.token = token

    @staticmethod
    def user_login(rid, password):
        error_code = 0
        res = db.getCard(rid, password).get_json()
        if 'msg' in res:
            error_code = 1
            return error_code, None
        else:
            return error_code, User(rid, res['name'])

    # 顾客设置空调开关
    @staticmethod
    def turn_on_off(rid, state):
        error_code = 0
        print(rid)
        if state != Store[rid].__state:
            if state:
                Store[rid].Turnon()
            else:
                Store[rid].Turnoff()
        return error_code

    # 顾客设置温度
    @staticmethod
    def set_temp(rid, temp):
        error_code = 0
        Store[rid].settemp(temp)
        return error_code

    # 顾客设置风速
    @staticmethod
    def set_mode(rid, mode):
        error_code = 0
        Store[rid].setmode(mode)
        return error_code

    # 顾客查看当前消费金额
    @staticmethod
    def show_cost(rid):
        error_code = 0
        # 空调开关状态
        onoff = Store[rid].__state
        Store[rid].updatecost()
        cost = Store[rid].cost
        return error_code, str(onoff), str(cost)

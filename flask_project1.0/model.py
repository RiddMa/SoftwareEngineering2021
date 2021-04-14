from collections import defaultdict
import time, datetime
import db
import json

class Acunit:
    def __init__(self,rid,state,temp,mode,last,cost,discount):
        #房号
        self.rid = rid
        #开关状态
        self.state = state
        #温度
        self.temp = temp
        #风速
        self.mode = mode
        #上次结算金额时间
        self.last = last
        #运行到现在的金额
        self.cost = cost
        #当前折扣
        self.discount = discount
        #总使用时长
        self.totaltime = 0
        #本次开机的时间
        self.starttime

    def settemp(self,newtemp):
        self.temp = newtemp
        return
    
    def changecost(self,deltcost):
        self.cost += deltcost
        return

    def changelasttime(self,newtime):
        self.totaltime += newtime - self.last
        self.last = newtime
        return

    def changediscount(self,discount):
        self.discount = discount
        return

    def setmode(self,newmode):
        newtime = time.time()
        self.changecost(self.Costcalc(newtime - self.last))
        self.changelasttime(newtime)
        self.mode = newmode
        return

    def Costcalc(self,time):
        switch = {'H': 0.03,'M': 0.02,'L': 0.01}
        res = switch[self.mode] * time / 60 * self.discount
        return res

    def updatecost(self):
        timenow = time.time()
        self.changecost(self.Costcalc(timenow - self.last))
        self.changelasttime(timenow)

    def Turnon(self):
        self.state = 1
        self.cost = 0.5
        newtime = time.time()
        self.last = newtime
        self.starttime = newtime
        return

    def Turnoff(self):
        self.state = 0
        newtime = time.time()
        self.changecost(self.Costcalc(newtime - self.last))
        self.changelasttime(newtime)
        addBill(rid,self.starttime,self.last,cost)
        return

roomlist = []
for j in range(1,6):
    for i in range(1,11):
        roomlist.append(str(j) + ('0' + str(i))[-2:])
roomstate = {i : 0 for i in roomlist}
Store = { i : Acunit(i,0,23,'L',int(time.time()),0,1.0) for i in roomlist}

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
        res = json.loads(getUser(username,password))
        if 'userid' in res:
            return error_code, Admin(res['userid'],username,password,'token')
        else:
            error_code = 1
        return error_code, Admin(0,'gg','gg','gg')

    # 生成报表，根据当前时间查询当前所有房间空调状态(开关、温度、风速等)与折扣
    @staticmethod
    def get_report(time):
        error_code = 0
        # 房间信息列表(空调状态与折扣)
        reslist = []
        for rid,value in Store.items():
            tpvar = dict()
            tpvar['rid'] = rid
            tpvar['state'] = value.state
            tpvar['temp'] = value.temp
            tpvar['mode'] = value.mode
            tpvar['discount'] = value.discount
            reslist.append(tpvar)
        return error_code, reslist

    #这里我不太理解流水是啥，接口可能设置不正确
    #应该是每天的实际入账金额，先空着
    @staticmethod
    def water_bills(time):
        error_code = 1
        starttime = time // 60 // 24 * 60 * 24
        endtime = time // 60 // 24 * 60 * 24 + 60 * 24
        return error_code, res

    #设置某个房间的折扣
    @staticmethod
    def set_discount(rid, discount):
        error_code = 0
        if Store[rid].state == 0:
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
            if Store[i].state != state:
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


'''
class Reception:
    # 根据预留电话号码返回一个房卡对象
    @staticmethod
    def get_card(phonenumber):
        error_code = 0
        return error_code, Orderedcards[phonenumber]

    # 退房结算
    @staticmethod
    def get_total_cost(rid):
        error_code = 0
        if Store[rid].state == 1:
            Store[rid].Turnoff()
        # 使用时间
        duration = Store[rid].totaltime
        # 消费金额
        price = Store[rid].cost
        return error_code, str(duration), str(price)
'''

class User:

    # 顾客设置空调开关
    @staticmethod
    def user_login(rid,password):
        error_code = 0
        res = json.loads(getUser(rid,password))
        if 'msg' in res:
            error_code = 1
        else:
            return error_code,res['username']

    @staticmethod
    def turn_on_off(rid, state):
        error_code = 0
        if state != Store[rid].state:
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
        onoff = Store[rid].state
        Store[rid].updatecost()
        cost = Store[rid].cost
        return error_code, str(onoff), str(cost)

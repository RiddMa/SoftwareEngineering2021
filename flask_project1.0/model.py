import random
import threading
import time
from datetime import datetime
from threading import Timer
import database

#todo
'''
 详单数量不对
 token
'''


SHUT_DOWN = 0
SET_MODE = 1
READY = 2
UNIT_FEE = 1
SPEED = dict([('0', 1 / 60), ('1', 2 / 60), ('2', 3 / 60)])
INIT_TEMP = dict([('101',26),('102',26),('103',26),('104',26)])


class WorkQueue:
    def __init__(self):
        self.array = []

    def __setitem__(self,key,value):
        self.array[key] = value

    def __getitem__(self,item):
        return self.array[item]

    def append(self,item):
        self.array.append(item)

    def remove(self,item):
        self.array.remove(item)

    def len(self):
        return len(self.array)

    def pop(self,key):
        self.array.pop(key)


waiting_queue = WorkQueue()
serving_queue = WorkQueue()


class Roomlist:
    def __init__(self):
        self.set = dict()

    def check(self,roomid):
        return roomid in self.set

    def __getitem__(self, item):
        return self.set[item]

    def __setitem__(self, key, value):
        self.set[key] = value


room_list = Roomlist()


class Detailedlist:
    def __init__(self):
        self.list = dict()

    def clear(self,roomid):
        self.list[roomid].clear()

    def deltaprice(self,roomId):
        delta = room_list[roomId].price
        if len(self.list[roomId]) > 0:
            delta -= self.list[roomId][-1]['Fee']
        return delta

    def insert(self, roomId, requesttime, requestduration, wind, fee):
        """
        返回格式：
        "RoomId": row.rid,                          #string
        "RequestTime": row.starttime, 			    #datetime    上次进服务队列的时间（没有就返回None）
        "RequestDuration" : row.duration,           #int（这次产生详单与上次产生详单，在服务队列的时间长度，以秒为单位）
        "FanSpeed": row.fanspeed, 					#char  "0","1","2"分别为低中高风速
        "FeeRate": feerate,							#float（每秒费用）
        "Fee": fee									#float（与上次产生详单之间，新产生的费用）
        :param fee:费用
        :param wind:风速
        :param requestduration:请求间隔
        :param requesttime:上次进入服务队列的时间
        :param roomId:房间号
        :return:
        """
        unit = dict([
            ('RoomId', roomId), ('RequestTime', requesttime.strftime("%Y-%m-%d %H:%m:%S")), ('requestduration', requestduration),
            ('FanSpeed', wind),
            ('FeeRate', SPEED[wind]), ('Fee', fee)
        ])
        if len(self.list[roomId]) > 0:
            unit['Fee'] -= self.list[roomId][-1]['Fee']
        self.list[roomId].append(unit)
        database.addbill(unit['Roomid'],unit['RequestTime'],unit['requestduration'],
                         unit['FanSpeed'],unit['FeeRate'],unit['Fee'])
        return


detailed_list = Detailedlist()


class Room:
    """
    描述房间的类，在本设计中与该房间内的空调绑定
    房间ID：roomId
    累计价格：cost
    计费率：feeRate
    目标温度：target_temp
    当前温度：current_temp
    风速：wind
    模式：mode
    开关机:state
    开机时间:start_time
    """

    def __init__(self, roomId, target_temp, current_temp, wind, mode, state, price):
        self.roomId = roomId
        self.feeRate = SPEED[wind] * UNIT_FEE
        self.wind = wind
        self.mode = mode
        self.target_temp = target_temp
        self.current_temp = current_temp
        self.last_settle_time = datetime.now()
        self.start_time = datetime.now()
        self.price = price
        self.state = state

    def settle(self):
        """
        按当前时间进行状态结算
        :return:
        """
        new_time = datetime.now()
        delt_time = (new_time - self.last_settle_time).microseconds / 1e6
        self.last_settle_time = new_time
        if not (self.roomId in waiting_queue) and not (self.roomId in serving_queue):
            # 关机状态
            new_temp = delt_time * 0.5 / 60
            if self.current_temp > INIT_TEMP[self.roomId]:
                new_temp = max(self.current_temp - new_temp, INIT_TEMP[self.roomId])
            else:
                new_temp = min(self.current_temp + new_temp, INIT_TEMP[self.roomId])
            self.current_temp = new_temp
            return
        if self.roomId in serving_queue:
            new_temp = delt_time * SPEED[self.wind]
            if self.mode == 0:
                if self.target_temp >= self.current_temp:
                    new_temp = self.current_temp
                else :
                    new_temp = max(self.current_temp - new_temp, self.target_temp)
            else:
                if self.target_temp <= self.current_temp:
                    new_temp = self.current_temp
                else :
                    new_temp = min(self.current_temp + new_temp, self.target_temp)
            self.price += (new_temp - self.current_temp)
            self.current_temp = new_temp
        return

    def SetTemp(self, temp):
        """
        修改房间设定温度
        :param temp:
        :return:
        """
        self.target_temp = temp

    def SetSpeed(self, speed):
        """
        修改房间设定风速
        :param speed:
        :return:
        """
        self.wind = speed

    def GetTemp(self):
        """
        获得房间温度
        :param roomId:
        :return:
        """
        return self.current_temp

    def SetPower(self,state):
        """
        设定开关机状态
        :param state: 新状态
        :return:
        """
        self.state = state

    def On(self):
        return self.state


class CentralAirConditioner:
    """
    描述中央空调的类
    状态：state
    Mode：初始模式
    Temp_highLimit：温度上限
    Temp_lowLimit：温度下限
    default_TargetTemp：初始温度
    FeeRate_H：高风速费用
    FeeRate_M：中风速费用
    FeeRate_L：低风速费用
    """

    def __init__(self):
        self.state = SHUT_DOWN
        self.mode = 0
        self.temp_highlimit = 27
        self.temp_lowlimit = 16
        self.default_targettemp = 25
        self.high_fee = 3 / 60
        self.mid_fee = 2 / 60
        self.low_fee = 1 / 60
        self.wind = 1

    def setState(self, mode):
        """
        更改中央空调状态
        :return:
        """
        self.state = mode

    def setPara(self, Mode, Temp_highLimit, Temp_lowLimit, default_TargetTemp, Wind,FeeRate_H, FeeRate_M, FeeRate_L):
        """
        :param Wind: 风速
        :param Mode: 初始模式
        :param Temp_highLimit:温度上限
        :param Temp_lowLimit:温度下限
        :param default_TargetTemp:初始温度
        :param FeeRate_H:高风速费用
        :param FeeRate_M:中风速费用
        :param FeeRate_L:低风速费用
        :return:
        """
        if Mode == 1:
            Mode = 0
        else:
            Mode = 1
        self.mode = Mode
        self.temp_highlimit = Temp_highLimit
        self.temp_lowlimit = Temp_lowLimit
        self.default_targettemp = default_TargetTemp
        self.wind = Wind
        self.high_fee = FeeRate_H
        self.mid_fee = FeeRate_M
        self.low_fee = FeeRate_L


central_ac = CentralAirConditioner()


class ClientController:
    """
    客户服务的控制器，用以响应客户的操作
    """

    @staticmethod
    def PowerOn(roomid):
        """
        响应空调开机操作，并转发请求到服务控制器
        :param roomid:房间号
        :param currentTemp:当前温度
        :return:roomstate
        """
        return ServerController.PowerOn(roomid)

    @staticmethod
    def RequestState(roomid):
        """
        响应状态查询操作并更新金额，并转发请求到服务控制器
        :param roomid:
        :return:
        """
        error_code = 0
        return error_code, ServerController.RequestState(roomid)

    @staticmethod
    def ChangeTargetTemp(roomId, targetTemp):
        """
        响应温度改变操作，并转发请求到服务控制器
        :param roomId:
        :param targetTemp:
        :return:
        """
        error_code = 0
        ServerController.ChangeTargetTemp(roomId, targetTemp)
        return error_code

    @staticmethod
    def ChangeFanSpeed(roomId, fanSpeed):
        """
        响应风速改变操作，并转发请求到服务控制器
        :param roomId:
        :param fanSpeed:
        :return:
        """
        error_code = 0
        ServerController.ChangeFanSpeed(roomId, fanSpeed)
        return error_code

    @staticmethod
    def PowerOff(roomId):
        """
        响应空调关机操作，并转发请求到服务控制器
        :param roomId:
        :return:
        """
        error_code = 0
        ServerController.PowerOff(roomId)
        return error_code


class SchedulingController:
    """
    调度控制器，用以进行空调调度操作
    """
    last_in_serving = dict()
    last_in_wating = dict()
    time_in_serving = dict()

    @staticmethod
    def Initialize():
        """
        调度控制器初始化
        :return:
        """
        error_code = 0
        return error_code

    @staticmethod
    def StartUp():
        """
        调度控制器启动
        :return:
        """
        error_code = 0
        return error_code

    @staticmethod
    def check(roomid):
        """
        定时状态修改
        :return:
        """
        if not roomid in serving_queue:
            return
        if (datetime.now() - SchedulingController.last_in_serving[roomid]).seconds < 120:
            return
        if waiting_queue.len() == 0:
            return
        waiting_queue.sort(key=lambda x: (room_list[x].wind, SchedulingController.last_in_wating[room_list[x].roomid]))
        if room_list[waiting_queue[0]].wind == room_list[roomid]:
            res = waiting_queue[0]
            serving_queue.remove(roomid)
            detailed_list.insert(roomid, SchedulingController.last_in_serving[roomid],
                                 SchedulingController.time_in_serving[roomid], room_list[roomid].wind, room_list[roomid].price)
            waiting_queue.remove(res)
            serving_queue.append(res)
            waiting_queue.append(roomid)
            SchedulingController.last_in_wating[roomid] = datetime.now()
            SchedulingController.last_in_serving[res] = datetime.now()
        SchedulingController.AddRoom(roomid)
        return

    @staticmethod
    def AddRoom(roomId):
        """
        新增服务对象
        :param roomId:
        :param price:
        :return:
        """
        if serving_queue.len() < 3:
            serving_queue.append(roomId)
            SchedulingController.last_in_serving[roomId] = datetime.now()
            return
        serving_queue.sort(key=lambda x: (room_list[x].wind, SchedulingController.last_in_serving[room_list[x].roomid]))
        if room_list[serving_queue[0]].wind < room_list[roomId].wind:
            room_list[serving_queue[0]].settle()
            room_list[roomId].settle()
            res = serving_queue[0]
            detailed_list.insert(res, SchedulingController.last_in_serving[res],
                                 SchedulingController.time_in_serving[res], room_list[res].wind, room_list[res].price)
            serving_queue[0], roomId = roomId, serving_queue[0]
            tr = Timer(120, SchedulingController.check)
            tr.start()
            SchedulingController.last_in_serving[serving_queue[0]] = datetime.now()
        waiting_queue.append(roomId)
        SchedulingController.last_in_wating[roomId] = datetime.now()
        return

    @staticmethod
    def move_out(roomId):
        """
        新增服务对象
        :param roomId:
        :param price:
        :return:
        """
        if roomId in waiting_queue:
            waiting_queue.remove(roomId)
            return
        if roomId in serving_queue:
            serving_queue.remove(roomId)
            detailed_list.insert(roomId, SchedulingController.last_in_serving[roomId],
                                 SchedulingController.time_in_serving[roomId], room_list[roomId].wind, room_list[roomId].price)
            if waiting_queue.len() == 0:
                return
            waiting_queue.sort(key=lambda x: (room_list[x].wind, SchedulingController.last_in_wating[room_list[x].roomid]))
            serving_queue.append(waiting_queue[0])
            SchedulingController.last_in_serving[waiting_queue[0]] = datetime.now()
            waiting_queue.pop(0)
        return


class ServerController:
    """
    服务器的控制器，用以各类服务器响应的操作
    """

    @staticmethod
    def PowerOn(roomId, current_temp, wind):
        """
        响应空调开机操作
        :param wind:
        :param current_temp:
        :param roomId:
        :return:error_code
        """
        # todo battle
        if room_list[roomId].On():
            error_code = 1
            return error_code
        room_list[roomId].SetPower(1)
        room_list[roomId].current_temp = current_temp
        room_list[roomId].wind = wind
        SchedulingController.AddRoom(roomId)
        detailed_list.list[roomId].clear()
        error_code = 0
        return error_code

    @staticmethod
    def RequestState(roomId):
        """
        响应状态查询操作并更新金额
        :param roomId:
        :return:
        """
        room_list[roomId].settle()
        return room_list[roomId]

    @staticmethod
    def ChangeTargetTemp(roomId, targetTemp):
        """
        响应温度改变操作
        :param roomId:
        :param targetTemp:
        :return:
        """
        if not room_list[roomId].On():
            return 1
        if targetTemp > central_ac.temp_highlimit or targetTemp < central_ac.temp_lowlimit:
            return 1
        SchedulingController.move_out(roomId)
        room_list[roomId].SetTemp(targetTemp)
        SchedulingController.AddRoom(roomId)
        return 0

    @staticmethod
    def ChangeFanSpeed(roomId, fanSpeed):
        """
        响应风速改变操作
        :param fanSpeed:
        :return:
        """
        if not room_list[roomId].On():
            return 1
        database.
        SchedulingController.move_out(roomId)
        room_list[roomId].SetSpeed(fanSpeed)
        SchedulingController.AddRoom(roomId)
        return 0

    @staticmethod
    def PowerOff(roomId):
        """
        响应空调关机操作
        :return:
        """
        if not room_list[roomId].On():
            return 1
        else:
            detailed_list.clear(roomId)
        SchedulingController.move_out(roomId)
        detailed_list.insert(roomId, SchedulingController.last_in_serving[roomId],
                             SchedulingController.time_in_serving[roomId], room_list[roomId].wind,
                             room_list[roomId].price)
        room_list[roomId].SetPower(0)
        return 0

    @staticmethod
    def CreateInvoice(RoomId):
        """
        响应创建帐单请求
        :param date_in:
        :param date_out:
        :return:
        """
        # todo 数据库中查询入住时间
        res = database.getbills(RoomId,datetime.now()).get_json()
        return dict([
            ('RoomId', RoomId), ('Total_Fee', res['price'] + detailed_list.deltaprice(RoomId)), ('date_in',res['time']),
            ('date_out', datetime.now().strftime("%Y-%m-%d %H:%m:%S"))
        ])

    @staticmethod
    def CreateRDR(RoomId):
        """
        响应创建详单请求
        """
        res = database.getbill(RoomId,datetime.now()).get_json()
        if 'msg' in res:
            return []
        return res

    @staticmethod
    def CheckRoomState(list_Room):
        """
        获取房间状态
        :return:
        """
        res_list = []
        for roomId in list_Room:
            unit = dict()
            unit['roomId'] = roomId
            if roomId in serving_queue:
                unit['state'] = 'server'
            elif roomId in waiting_queue:
                unit['state'] = 'wait'
            else:
                unit['state'] = 'tempUp'
            if room_list[roomId].mode == 0:
                unit['mode'] = 1
            else:
                unit['mode'] = -1
            unit['targetTemp'] = room_list[roomId].target_temp
            unit['currentTemp'] = room_list[roomId].current_temp
            unit['fanSpeed'] = room_list[roomId].wind
            res_list.append(unit)
        error_code = 0
        return error_code, res_list

    @staticmethod
    def PowerON():
        """
        响应中央空调开机
        :return:错误码
        """
        global central_ac, waiting_queue, serving_queue
        if central_ac.state != SHUT_DOWN:
            error_code = 1
            return error_code
        central_ac = CentralAirConditioner()
        central_ac.setState(SET_MODE)
        SchedulingController.Initialize()
        waiting_queue = WorkQueue()
        serving_queue = WorkQueue()
        error_code = 0
        return error_code

    @staticmethod
    def update():
        while central_ac.state != SHUT_DOWN:
            time.sleep(0.2)
            for roomid in room_list:
                room_list[roomid].settle()
                if roomid in serving_queue:
                    SchedulingController.time_in_serving[roomid] += 1
                    if room_list[roomid].current_temp == room_list[roomid].target_temp:
                        SchedulingController.move_out(roomid)
                    elif room_list[roomid].mode == 0 and room_list[roomid].current_temp < room_list[roomid].target_temp:
                        SchedulingController.move_out(roomid)
                    elif room_list[roomid].mode == 1 and room_list[roomid].current_temp > room_list[roomid].target_temp:
                        SchedulingController.move_out(roomid)
                else:
                    SchedulingController.time_in_serving[roomid] = 0
                    if (roomid not in waiting_queue) and (roomid not in serving_queue):
                        if room_list[roomid].current_temp - room_list[roomid].target_temp > 1 \
                                and room_list[roomid].mode == 0:
                            SchedulingController.AddRoom(roomid)
                        elif room_list[roomid].current_temp - room_list[roomid].target_temp < -1 \
                                and room_list[roomid].mode == 1:
                            SchedulingController.AddRoom(roomid)
        return

    @staticmethod
    def StartUp():
        """
        响应中央空调的起步
        :return:错误码
        """
        global central_ac, room_list
        if central_ac.state != SET_MODE:
            return 1
        central_ac.setState(READY)
        central_ac.state = READY
        room_list = dict()
        for i in range(1, 6):
            for j in range(1, 11):
                roomId = str(i * 100 + j)
                room_list[roomId] = Room(roomId, central_ac.default_targettemp, 26, central_ac.wind, 0, 0, 0)
                SchedulingController.last_in_serving[roomId] = SchedulingController.last_in_wating[roomId] = None
                detailed_list.list[roomId] = []
                SchedulingController.time_in_serving[roomId] = 0
                if roomId not in INIT_TEMP:
                    INIT_TEMP[roomId] = 26
        room_list['101'].current_temp = INIT_TEMP['101']
        room_list['102'].current_temp = INIT_TEMP['102']
        room_list['103'].current_temp = INIT_TEMP['103']
        room_list['104'].current_temp = INIT_TEMP['104']
        tr = threading.Thread(target=ServerController.update)
        tr.start()
        return 0

    @staticmethod
    def setPara(Mode, Temp_highLimit, Temp_lowLimit, default_TargetTemp, Wind, FeeRate_H, FeeRate_M, FeeRate_L):
        """
        响应赋值空调的缺省工作模式，包括初始温度，温度上限下限，不同风速的费率等
        :param Wind: 默认风速
        :param Mode: 初始模式
        :param Temp_highLimit:温度上限
        :param Temp_lowLimit:温度下限
        :param default_TargetTemp:初始温度
        :param FeeRate_H:高风速费用
        :param FeeRate_M:中风速费用
        :param FeeRate_L:低风速费用
        :return:错误码
        """
        global central_ac
        if central_ac.state != SET_MODE:
            return 1
        central_ac.setPara(Mode, Temp_highLimit, Temp_lowLimit, default_TargetTemp,Wind, FeeRate_H, FeeRate_M, FeeRate_L)
        return 0

    @staticmethod
    def queryreport(Roomid, type_Report, date1, date2):

        return dict()


class log:
    """
    登陆管理的类
    实例属性：用户名和密码
    类属性：token_pool,一个用来存储token和帐号对应用户名和类型
    方法：
    """
    token_pool = [i for i in range(1, 10)]

    @staticmethod
    def stuff_login(username: str, password: str, privilege):
        """
        用于登陆的方法，过程中需要校验用户名和密码
        :param username: 传入的工作人员用户名
        :param password: 工作人员密码
        :return: error_code、token和该工作人员的类型/权限
        需要校验数据库中是否有账号信息，是否已登陆，和权限是否对的上
        """
        error_code = 0
        return error_code

    @staticmethod
    def custom_login(username: str, password: str):
        """
        用于生成空调管理人员token的方法
        :param username:用户名
        :param password:密码
        :return:token
        """
        error_code = 0
        return error_code, log.token_pool[random.randint(0, len(log.token_pool) - 1)]

    @staticmethod
    def check_token(token):
        return token in log.token_pool


class ManagerController:
    @staticmethod
    def Queryreport(Roomid, type_Report, date1, date2):
        error_code = 0
        return error_code,ServerController.queryreport(Roomid, type_Report, date1, date2)


class ReceptionController:
    @staticmethod
    def CreateInvoice(RoomId):
        error_code = 0
        return error_code,ServerController.CreateInvoice(RoomId)

    @staticmethod
    def CreateRDR(RoomId):
        error_code = 0
        return error_code,ServerController.CreateRDR(RoomId)

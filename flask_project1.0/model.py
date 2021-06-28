import random
import threading
import time
from datetime import datetime
from threading import Timer
import database

SHUT_DOWN = 0
SET_MODE = 1
READY = 2
UNIT_FEE = 1
SPEED = dict([('0', 5 / 60), ('1', 20 / 120), ('2', 5 / 180)])
INIT_TEMP = dict([('101', 32), ('102', 28), ('103', 27), ('104', 29)])


class WorkQueue:
    def __init__(self):
        self.array = []

    def __setitem__(self, key, value):
        self.array[key] = value

    def __getitem__(self, item):
        return self.array[item]

    def append(self, item):
        self.array.append(item)

    def remove(self, item):
        self.array.remove(item)

    def len(self):
        return len(self.array)

    def pop(self, key):
        self.array.pop(key)


waiting_queue = WorkQueue()
serving_queue = WorkQueue()


class Roomlist:
    def __init__(self):
        self.set = dict()

    def check(self, roomid):
        return roomid in self.set

    def __getitem__(self, item):
        return self.set[item]

    def __setitem__(self, key, value):
        self.set[key] = value


room_list = Roomlist()


class Detailedlist:
    def __init__(self):
        self.list = dict()

    def clear(self, roomid):
        self.list[roomid].clear()

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
        tp = requesttime
        if tp is None:
            tp = datetime.strptime('2000-01-01 00:00:00', '%Y-%m-%d %H:%m:%S')
        unit = dict([
            ('RoomId', roomId), ('RequestTime', tp.strftime("%Y-%m-%d %H:%m:%S")),
            ('requestduration', requestduration),
            ('FanSpeed', wind),
            ('FeeRate', SPEED[wind]), ('Fee', fee)
        ])
        room_list[roomId].price = 0  # 清空price
        self.list[roomId].append(unit)
        return database.adddr(room=unit['RoomId'], time1=tp, time2=unit['requestduration'],
                              time=datetime.now(), speed=unit['FanSpeed'], feerate=unit['FeeRate'], cost=unit['Fee'])


detailed_list = Detailedlist()


class Room:
    """
    描述房间的类，在本设计中与该房间内的空调绑定
    房间ID：roomId
    本次开机累计价格：cost (关机清空)
    上次生成详单到现在的价格：price (每次生成详单后清空)
    计费率：feeRate
    目标温度：target_temp
    当前温度：current_temp
    风速：wind
    模式：mode
    开关机:state
    开机时间:start_time
    """

    def __init__(self, roomId, target_temp, current_temp, wind: str, mode, state, price):
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
        self.cost = 0

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
            # print('delt',delt_time,'new',new_temp)
            if self.mode == 0:
                if self.target_temp >= self.current_temp:
                    new_temp = self.current_temp
                else:
                    new_temp = max(self.current_temp - new_temp, self.target_temp)
            else:
                if self.target_temp <= self.current_temp:
                    new_temp = self.current_temp
                else:
                    new_temp = min(self.current_temp + new_temp, self.target_temp)
            self.price += abs(new_temp - self.current_temp)
            self.cost += abs(new_temp - self.current_temp)
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

    def SetPower(self, state):
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
        self.wind = "1"

    def setState(self, mode):
        """
        更改中央空调状态
        :return:
        """
        self.state = mode

    def setPara(self, Mode, Temp_highLimit, Temp_lowLimit, default_TargetTemp, Wind, FeeRate_H, FeeRate_M, FeeRate_L):
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
        waiting_queue.array.sort(key=lambda x: (room_list[x].wind, SchedulingController.last_in_wating[x]))
        if room_list[waiting_queue[0]].wind == room_list[roomid]:
            res = waiting_queue[0]
            serving_queue.remove(roomid)
            detailed_list.insert(roomid, SchedulingController.last_in_serving[roomid],
                                 SchedulingController.time_in_serving[roomid], room_list[roomid].wind,
                                 room_list[roomid].price)
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
        :return:
        """
        if serving_queue.len() < 3:
            serving_queue.append(roomId)
            SchedulingController.last_in_serving[roomId] = datetime.now()
            return
        serving_queue.array.sort(key=lambda x: (room_list[x].wind, SchedulingController.last_in_serving[x]))
        if room_list[serving_queue[0]].wind < room_list[roomId].wind:
            room_list[serving_queue[0]].settle()
            room_list[roomId].settle()
            res = serving_queue[0]
            detailed_list.insert(res, SchedulingController.last_in_serving[res],
                                 SchedulingController.time_in_serving[res], room_list[res].wind, room_list[res].price)
            serving_queue[0], roomId = roomId, serving_queue[0]
            '''
            取消时间片
            tr = Timer(120, SchedulingController.check)
            tr.start()
            '''
            SchedulingController.last_in_serving[serving_queue[0]] = datetime.now()
        waiting_queue.append(roomId)
        SchedulingController.last_in_wating[roomId] = datetime.now()
        return

    @staticmethod
    def move_out(roomId):
        """
        新增服务对象
        :param roomId:
        :return:
        """
        if roomId in waiting_queue:
            waiting_queue.remove(roomId)
            return
        if roomId in serving_queue:
            serving_queue.remove(roomId)
            res = detailed_list.insert(roomId, SchedulingController.last_in_serving[roomId],
                                       SchedulingController.time_in_serving[roomId], room_list[roomId].wind,
                                       room_list[roomId].price)
            print('res', res)
            if waiting_queue.len() == 0:
                return
            waiting_queue.array.sort(key=lambda x: (room_list[x].wind, SchedulingController.last_in_wating[x]))
            serving_queue.append(waiting_queue[0])
            SchedulingController.last_in_serving[waiting_queue[0]] = datetime.now()
            waiting_queue.pop(0)
        return


class ServerController:
    """
    服务器的控制器，用以各类服务器响应的操作
    """

    @staticmethod
    def PowerOn(roomId: str, current_temp, wind):
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
        database.addrecord(roomId, 0, datetime.now())
        room_list[roomId].SetPower(1)
        # room_list[roomId].current_temp = current_temp
        room_list[roomId].wind = central_ac.wind
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
        res = room_list[roomId]
        res.price += database.asktotalfee(roomId, datetime.now()).get_json()['price']
        return res

    @staticmethod
    def ChangeTargetTemp(roomId, targetTemp):
        """
        响应温度改变操作
        :param roomId:
        :param targetTemp:
        :return:
        """
        if type(targetTemp) != int:
            return 1
        if not room_list[roomId].On():
            return 1
        if targetTemp > central_ac.temp_highlimit or targetTemp < central_ac.temp_lowlimit:
            return 1
        database.addrecord(roomId, 3, datetime.now())
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
        if fanSpeed not in ['0', '1', '2']:
            return 1
        if not room_list[roomId].On():
            return 1
        database.addrecord(roomId, 2, datetime.now())
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
        if central_ac.state != READY:
            return 1
        if not room_list[roomId].On():
            return 1
        database.addrecord(roomId, 1, datetime.now())
        SchedulingController.move_out(roomId)
        # detailed_list.insert(roomId, SchedulingController.last_in_serving[roomId],
        #                     SchedulingController.time_in_serving[roomId], room_list[roomId].wind,
        #                     room_list[roomId].price)
        room_list[roomId].SetPower(0)
        room_list[roomId].cost = 0
        detailed_list.clear(roomId)
        return 0

    @staticmethod
    def CreateInvoice(RoomId):
        """
        响应创建帐单请求
        :param RoomId
        :return:
        """
        # todo 数据库中查询入住时间
        # res = database.getbills(RoomId,datetime.now()).get_json()
        print(database.asktotalfee(RoomId, datetime.now()).get_json())
        return dict([
            ('RoomId', RoomId), ('Total_Fee',
                                 room_list[RoomId].price + database.asktotalfee(RoomId, datetime.now()).get_json()[
                                     'price']
                                 ), ('date_in', datetime.now().strftime("%Y-%m-%d %H:%m:%S")),
            ('date_out', datetime.now().strftime("%Y-%m-%d %H:%m:%S"))
        ])

    @staticmethod
    def CreateRDR(RoomId):
        """
        响应创建详单请求
        """
        res = database.askdr(RoomId, datetime.now()).get_json()
        print(res)
        if 'msg' in res:
            return []
        return res

    @staticmethod
    def CheckRoomState():
        """
        获取房间状态
        :return:
        """
        res_list = []
        for roomId in room_list:
            if not room_list[roomId].On():
                continue
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
        delt = 0.2
        t = 0
        for i in room_list:
            print('temp', i, '; ', room_list[i].current_temp, 'S:', i in serving_queue, 'W:', i in waiting_queue)
        while central_ac.state != SHUT_DOWN:
            time.sleep(delt)
            for roomid in room_list:
                room_list[roomid].settle()
                if roomid in serving_queue:
                    SchedulingController.time_in_serving[roomid] += delt
                    if room_list[roomid].current_temp == room_list[roomid].target_temp:
                        SchedulingController.move_out(roomid)
                    elif room_list[roomid].mode == 0 and room_list[roomid].current_temp < room_list[roomid].target_temp:
                        SchedulingController.move_out(roomid)
                    elif room_list[roomid].mode == 1 and room_list[roomid].current_temp > room_list[roomid].target_temp:
                        SchedulingController.move_out(roomid)
                else:
                    SchedulingController.time_in_serving[roomid] = 0
                    if room_list[roomid].On() and (roomid not in waiting_queue) and (roomid not in serving_queue):
                        if room_list[roomid].current_temp - room_list[roomid].target_temp > 1 \
                                and room_list[roomid].mode == 0:
                            SchedulingController.AddRoom(roomid)
                        elif room_list[roomid].On() and room_list[roomid].current_temp - room_list[
                            roomid].target_temp < -1 \
                                and room_list[roomid].mode == 1:
                            SchedulingController.AddRoom(roomid)
                t = t + 1
                if t % 50 == 0:
                    for i in room_list:
                        print('temp', i, '; ', room_list[i].current_temp, 'S:', i in serving_queue, 'W:',
                              i in waiting_queue,'C:',room_list[i].cost)
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
        for i in range(1, 2):
            for j in range(1, 5):
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
        central_ac.setPara(Mode, Temp_highLimit, Temp_lowLimit, default_TargetTemp, Wind, FeeRate_H, FeeRate_M,
                           FeeRate_L)
        return 0

    @staticmethod
    def queryreport(Roomid, date1, date2):
        askres = database.askrecord(Roomid, date1, date2).get_json()

        res = dict([
            ('roomId', Roomid), ('changetemptimes', askres['count1']), ('changespeedtimes', askres['count2']),
            ('totalfee', room_list[Roomid].price + database.asktotalfee(Roomid, datetime.now()).get_json()['price']),
            ('powerofftimes', askres['count3']),
            ('ACworkingtime', askres['count4'])
        ])
        return res


class log:
    """
    登陆管理的类
    实例属性：用户名和密码
    类属性：token_pool,一个用来存储token和帐号对应用户名和类型
    方法：
    """
    token_pool = [str(i) for i in range(1, 10)]

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
        res = database.getUser(username,password,privilege).get_json()
        if 'msg' in res:
            error_code = 1
        return error_code

    @staticmethod
    def custom_login(username: str, password: str):
        """
        :param username:用户名
        :param password:密码
        :return:token
        """
        error_code = 0
        res = database.getUser(username,password,'0').get_json()
        if 'msg' in res:
            error_code = 1
        return error_code, log.token_pool[random.randint(0, len(log.token_pool) - 1)], INIT_TEMP[username]

    @staticmethod
    def check_token(token):
        return token in log.token_pool


class ManagerController:
    @staticmethod
    def Queryreport(Roomid, type_Report, date1, date2):
        error_code = 0
        return error_code, ServerController.queryreport(Roomid, type_Report, date1, date2)


class ReceptionController:
    @staticmethod
    def CreateInvoice(RoomId):
        error_code = 0
        return error_code, ServerController.CreateInvoice(RoomId)

    @staticmethod
    def CreateRDR(RoomId):
        error_code = 0
        return error_code, ServerController.CreateRDR(RoomId)

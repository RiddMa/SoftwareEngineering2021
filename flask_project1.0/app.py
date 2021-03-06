from flask import Flask, request, jsonify, make_response, sessions
import json
from flask_cors import CORS
from model import log, ClientController, ServerController, ReceptionController, ManagerController
from myglobal import app
import hashlib
import time
import datetime

CORS(app)

admin_tokens = set()
user_tokens = set()

def new_token(username):
    ctime = str(time.time())
    m = hashlib.md5(bytes(username, encoding="utf-8"))
    m.update(bytes(ctime, encoding="utf-8"))
    return m.hexdigest()


def set_token(is_admin, token):
    if is_admin:
        admin_tokens.add(token)
    else:
        user_tokens.add(token)


def verify_token(is_admin, token):
    if is_admin:
        return token in admin_tokens
    else:
        return token in user_tokens


@app.route('/')
def hello_world():
    return 'Hello World!'


# 顾客模块
@app.route('/api/usr/signup', methods=['POST'])
def enter_room():
    """
    用户进房
    请求参数
    roomId 房间号 string
    password 密码 string
    :return token: 众望所归 string
            currentTemp: 房间温度 int  说明：为迎合初始房间温度不同的设定，
            304e组选择将初始温度写进房间表中，在signup请求给出,在poweron时获取。
    :return:
    """
    res = dict([
        ('token',None),('currentTemp',None)
    ]
    )
    form = request.get_json()
    print(form)
    if 'roomId' in form:
        room_id = form['roomId']
    elif 'user' in form:
        room_id = form['user']
    else:
        error_code = 1
        return jsonify({'error_code': error_code})

    if 'password' in form:
        password = form['password']
    elif 'passwd' in form:
        password = form['passwd']
    else:
        error_code = 1
        return jsonify({'error_code': error_code})
    # TODO 调用用户登录函数
    error_code, token,current_temp = log.custom_login(room_id,password)

    if error_code == 1:
        return jsonify({'error_code': 1})

    res['token'] = token
    res['currentTemp'] = current_temp

    # set_token(False,res['token'])
    return jsonify({'error_code': error_code, 'data': res})


@app.route('/api/usr/poweron', methods=['POST'])
def user_poweron():
    """
    请求参数:
    roomId : 	房间号		string
    targetTemp：目标温度	int
    fanSpeed：	风速 		char 	"0","1","2"分别为低中高风速
    currentTemp:房间温度    int
    :return:无
    """
    room_id = None
    form = request.get_json()
    room_id = form['roomId']
    target_temp = int(form['targetTemp'])
    fan_speed = form['fanSpeed']
    if 'currentTemp' in form:
        current_temp = int(form['currentTemp'])
    # token = request.headers['authorization']
    #
    # if not verify_token(False, token):
    #     return jsonify({'error_code': 1})

    # TODO 调用用户开机函数
    error_code = ServerController.PowerOn(room_id, fan_speed)

    return jsonify({'error_code': error_code})


@app.route('/api/usr/requeststate', methods=['POST'])
def request_state():
    """
    心跳包
    请求参数：
    roomid：     房间号	    string
    :return:{"currentTemp":currentTemp，"totalFee":totalFee，"currentFee":currentFee}
    """
    form = request.get_json()
    room_id = form['roomId']
    # token = request.headers['authorization']
    #
    # if not verify_token(False, token):
    #     return jsonify({'error_code': 1})

    # TODO 调用用户查询使用空调情况的函数
    error_code, room = ClientController.RequestState(room_id)

    if error_code == 1:
        return jsonify({'error_code': 1})

    res = dict()
    res['currentTemp'] = room.current_temp
    # TODO 总费用与当前费用
    res['totalFee'] = room.calc
    res['currentFee'] = room.cost

    return jsonify({'error_code': error_code, 'data': res})


@app.route('/api/usr/changetargettemp', methods=['POST'])
def change_target_temp():
    """
    用户调温
    请求参数:
    roomid：		房间号			string
    targetTemp：	目标温度		int
    :return:无
    """
    form = request.get_json()
    room_id = form['roomId']
    target_temp = int(form['targetTemp'])
    # token = request.headers['authorization']
    #
    # if not verify_token(False, token):
    #     return jsonify({'error_code': 1})

    # TODO 调用用户设置目标温度函数
    error_code = ClientController.ChangeTargetTemp(room_id, target_temp)

    return jsonify({'error_code': error_code})


@app.route('/api/usr/changefanspeed', methods=['POST'])
def change_fan_speed():
    """
    用户调风
    请求参数:
    roomid：		房间号		string
    fanSpeed：		风速 		char 	"0","1","2"分别为低中高风速
    :return:无
    """
    form = request.get_json()
    room_id = form['roomId']
    fan_speed = form['fanSpeed']
    # token = request.headers['authorization']
    #
    # if not verify_token(False, token):
    #     return jsonify({'error_code': 1})

    # TODO 调用用户设置风速函数
    error_code = ClientController.ChangeFanSpeed(room_id, fan_speed)

    return jsonify({'error_code': error_code})


@app.route('/api/usr/poweroff', methods=['POST'])
def user_poweroff():
    """
    用户关机
    请求参数:
    roomid：	房间号		string
    :return:无
    """
    form = request.get_json()
    room_id = form['roomId']
    # token = request.headers['authorization']
    #
    # if not verify_token(False, token):
    #     return jsonify({'error_code': 1})

    # TODO 调用用户关机函数
    error_code = ClientController.PowerOff(room_id)

    return jsonify({'error_code': error_code})


# 前台模块
@app.route('/api/recp/signup', methods=['POST'])
def recp_login():
    """
    前台登录
    请求参数
    user:
    passwd:
    :return: token
    """
    form = request.get_json()
    username = form['user']
    password = form['passwd']

    # TODO 调用前台登录函数
    error_code = log.stuff_login(username,password,'2')

    if error_code == 1:
        return jsonify({'error_code': 1})

    res = dict()
    # res['token'] = token

    # set_token(False,res['token'])
    return jsonify({'error_code': error_code, 'data': res})


@app.route('/api/recp/createinvoice', methods=['POST'])
def create_invoice():
    """
    前台创建账单
    请求参数：
    roomid：	房间号		string
    :return:
    {
        "RoomId": rid, 				#string
        "Total_Fee": total_feel, 	#float
        "date_in": date_in,			#datetime
        "date_out": date_out		#datetime（查询的时候的系统时间）
    }
    """
    form = request.get_json()
    room_id = form['roomId']

    # TODO 调用前台打印账单函数
    error_code, invoice = ReceptionController.CreateInvoice(room_id)

    if error_code == 1:
        return jsonify({'error_code': 1})

    res = dict()
    res['RoomId'] = room_id
    res['Total_Fee'] = invoice['Total_Fee']
    res['date_in'] = invoice['date_in']
    res['date_out'] = invoice['date_out']

    return jsonify({'error_code': error_code, 'data': res})


@app.route('/api/recp/createrd', methods=['POST'])
def createrd():
    """
    前台创建详单
    请求参数：
    roomId：	房间号		string
    :return:
    [ {
        "RoomId": row.rid, 						#string
        "RequestTime": row.starttime, 			#datetime    上次进服务队列的时间（没有就返回None）
        "RequestDuration" : row.duration, 		#int（这次产生详单与上次产生详单，在服务队列的时间长度，以秒为单位）
        "FanSpeed": row.fanspeed, 				#char  "0","1","2"分别为低中高风速
        "FeeRate": feerate,						#float（每秒费用）
        "Fee": fee								#float（与上次产生详单之间，新产生的费用）
	} ]
    """
    form = request.get_json()
    print(form)
    room_id = form['roomId']

    # TODO 调用前台打印详单函数
    error_code, list = ReceptionController.CreateRDR(room_id)

    if error_code == 1:
        return jsonify({'error_code': 1,'data':[]})

    return jsonify({'error_code': error_code, 'data': list})


# 管理员模块
@app.route('/api/admin/signup', methods=['POST'])
def admin_login():
    """
    管理员登录
    请求参数
    user:
    passwd:
    :return: token
    """
    try:
        form = request.get_json()
        username = form['user']
        if 'passwd' in form:
            password = form['passwd']
        elif 'password' in form:
            password = form['password']
        else:
            error_code = 1
            return jsonify({'error_code': error_code})

    # TODO 调用管理员登录函数
        error_code = log.stuff_login(username,password,'1')

        if error_code == 1:
            return jsonify({'error_code': 1})

        res = dict()
        # res['token'] = token

        # set_token(False,res['token'])
        return jsonify({'error_code': error_code, 'data': res})
    except:
        return jsonify({'error_code': 1, 'data': dict()})

@app.route('/api/admin/poweron', methods=['POST'])
def admin_poweron():
    """
    管理员开机
    请求参数：
    无
    :return:无
    """
    res = dict()

    # TODO 调用管理员开机函数
    error_code = ServerController.PowerON()

    return jsonify({'error_code': error_code})


@app.route('/api/admin/setpara', methods=['POST'])
def set_param():
    """
    管理员设置中央空调参数
    请求参数：
    mode:				    模式 			    int			1，-1分别为制冷，制热
    temp_h:					最高可设定温度	    int
    temp_l:					最低可设定温度	    int
    defalut_targetTemp:		默认温度			int
    default_fanSpeed:		默认风速			char  		"0","1","2"分别为低中高风速
    feeRate_h:
    feeRate_m:
    feeRate_l:				高中低风速下费率    float		数值待定
    :return:无
    """
    form = request.get_json()
    mode = int(form['mode'])
    temp_h = int(form['temp_h'])
    temp_l = int(form['temp_l'])
    defalut_target_temp = int(form['default_targetTemp'])
    default_fan_speed = form['default_fanSpeed']

    fee_rate_h = float(form['feeRate_h'])
    fee_rate_m = float(form['feeRate_m'])
    fee_rate_l = float(form['feeRate_l'])

    # token = request.headers['authorization']
    #
    # if not verify_token(True, token):
    #     return jsonify({'error_code' : 1})

    # TODO 调用管理员设置中央空调参数函数
    error_code = ServerController.setPara(mode, temp_h, temp_l, defalut_target_temp, default_fan_speed,fee_rate_h, fee_rate_m, fee_rate_l)

    return jsonify({'error_code': error_code})


@app.route('/api/admin/startup', methods=['POST'])
def startup():
    """
    管理员运行中央空调
    请求参数：
    无
    :return: 无
    """

    # token = request.headers['authorization']
    #
    # if not verify_token(True, token):
    #     return jsonify({'error_code' : 1})

    # TODO 调用管理员管理员运行中央空调参数函数
    error_code = ServerController.StartUp()

    return jsonify({"error_code": error_code})


@app.route('/api/admin/checkroomstate', methods=['POST'])
def check_room_state():
    """
    管理员监视房间空调
    请求参数：
    list_Room:		希望监视的房间号列表	    list of string
    :return:
    [{
        roomId	:rid	           		string          希望生成报表的房间号
        "state":state					string			"server","wait","tempUp"
        "mode":mode,					int 			1,-1分别表制冷、制热
        "targetTemp":targetTemp,		int 			目标温度
        "currentTemp":currentTemp,		int				当前温度
        "fanSpeed":fanSpeed,			char			"0","1","2"分别为低中高风速
    }]
    """
    form = request.get_json()
    # TODO 不需要房间Id列表,直接返回所有房间

    # token = request.headers['authorization']
    #
    # if not verify_token(True, token):
    #     return jsonify({'error_code' : 1})

    # TODO 调用管理员监视房间空调
    error_code, state_list = ServerController.CheckRoomState()

    if error_code == 1:
        return jsonify({'error_code': 1})

    return jsonify({"error_code": error_code, "data": state_list})


#经理模块
@app.route('/api/mgr/signup', methods=['POST'])
def mgr_login():
    """
    经理登录
    请求参数
    user:
    passwd:
    :return: token
    """
    form = request.get_json()
    username = form['user']
    password = form['passwd']

    # TODO 调用经理登录函数
    error_code = log.stuff_login(username,password,'3')

    if error_code == 1:
        return jsonify({'error_code': 1})

    res = dict()
    # res['token'] = token

    # set_token(False,res['token'])
    return jsonify({'error_code': error_code, 'data': res})


@app.route('/api/mgr/createreport', methods=['POST'])
def create_report():
    """
    经理创建报表
    请求参数：
    roomId:		希望生成报表的房间号		l string
    date1:		报表开始时间				datetime
    date2:		报表结束时间				datetime
    :return:
    [	{
        roomId:rid                                  #string
        changetemptimes: row.changetemptimes, 		#int
        changespeedtimes: row.changespeedtimes, 	#int
        totalfee: row.totalfee,						#float
        powerofftimes: row.powerofftimes, 			#int
        DRnum: row.DRnum,							#int
        ACworkingtime: row.ACworkingtime		    #int
    }	]
    """
    form = request.get_json()
    room_id = form['roomId']
    start_date = datetime.datetime.strptime(form['date1'], "%Y-%m-%d %H:%M:%S")
    end_date = datetime.datetime.strptime(form['date2'], "%Y-%m-%d %H:%M:%S")
    # token = request.headers['authorization']
    #
    # if not verify_token(True, token):
    #     return jsonify({'error_code': 1})

    # TODO 调用经理创建报表函数
    error_code, report_list = ManagerController.Queryreport(room_id, start_date, end_date)

    # error_code = 0
    # report_list = [	{
    #     'roomId':'101',                                 #string
    #     'changetemptimes': 0, 		#int
    #     'changespeedtimes': 0, 	#int
    #     'totalfee': 0.0,						#float
    #     'powerofftimes': 0, 			#int
    #     'DRnum': 0,							#int
    #     'ACworkingtime': 0		    #int
    # }	]

    if error_code == 1:
        return jsonify({'error_code': 1})

    return jsonify({'error_code': error_code, 'data': report_list})


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)

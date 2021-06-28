from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask, jsonify, abort, make_response, current_app
import pymysql
from sqlalchemy.sql.functions import count
from sqlalchemy.sql.sqltypes import DateTime
from myglobal import app
import time
import datetime

# app=Flask(__name__) #创建1个Flask实例
# test
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:xzc19991208@localhost/rg"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:L1nQ1T@ng0xCC@localhost/soft"
# 指定当视图执行完毕后,自动提交数据库操作
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 指定每次执行操作时打印原始的SQL语句
# app.config['SQLALCHEMY_ECHO'] = True
# 防止jsonify出现中文乱码
app.config['JSON_AS_ASCII'] = False
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
mydb = SQLAlchemy(app)


class Room(mydb.Model):
    __tablename__ = 'room'
    userid = mydb.Column(mydb.String(255), nullable=False)
    roomid = mydb.Column(mydb.String(255), primary_key=True)
    password = mydb.Column(mydb.String(255), nullable=False)
    date = mydb.Column(mydb.String(255), nullable=False)  # 入住时间

    def __repr__(self):
        return '<Room %r>' % self.roomid  # = self.func_wxplhdyt()


class User(mydb.Model):
    __tablename__ = 'user'
    user_id = mydb.Column(mydb.String(255), nullable=False,primary_key=True)
    user_password = mydb.Column(mydb.String(255), nullable=False)
    user_name = mydb.Column(mydb.String(255), nullable=False)
    user_kind = mydb.Column(mydb.String(255), nullable=False,primary_key=True)  # 标识人员身份

    def __repr__(self):
        return '<User %r>' % self.user_id  # = self.func_wxplhdyt()


class Bill(mydb.Model):
    __tablename__ = 'bill'
    room = mydb.Column(mydb.String(255), nullable=False,primary_key=True)
    start_time = mydb.Column(mydb.String(255), nullable=False)
    during_time = mydb.Column(mydb.Float, nullable=False)
    time = mydb.Column(mydb.String(255), nullable=False,primary_key=True)
    speed = mydb.Column(mydb.String(255), nullable=False,)  # 风速
    feerate = mydb.Column(mydb.Float, nullable=False)  # 费率
    cost = mydb.Column(mydb.Float, nullable=False)  # 这段时间花费

    # kind = mydb.Column(mydb.Integer, primary_key=True)#1：调风，2：调温，3：两个都调,4：开关机
    def __repr__(self):
        return '<room %r>' % self.room


class Record(mydb.Model):
    __tablename__ = 'record'
    room = mydb.Column(mydb.String(255), nullable=False,primary_key=True)
    time = mydb.Column(mydb.String(255), nullable=False,primary_key=True)  # 当前时间
    kind = mydb.Column(mydb.Integer)  # 1：开机，2：关机，3：调温,4：调风

    def __repr__(self):
        return '<room %r>' % self.room


mydb.init_app(app)
with app.app_context():
    mydb.init_app(app)
    mydb.create_all(app=app)


def addrecord(roomid, kind, time):
    with app.app_context():
        time = time.strftime("%Y-%m-%d %H:%M:%S")
        record = Record(room=roomid, kind=kind, time=time)
        try:
            mydb.session.add(record)
            mydb.session.commit()
            result = {'msg': 'accept'}
        except:
            # 插入失败的话进行回滚
            mydb.session.rollback()
            mydb.session.flush()
            result = {'msg': '插入失败'}
    return jsonify(result)


def askrecord(roomid, stattime, endtime):
    with app.app_context():
        stattime = stattime.strftime("%Y-%m-%d %H:%M:%S")
        endtime = endtime.strftime("%Y-%m-%d %H:%M:%S")
        try:
            count1 = mydb.session.query(func.sum(Record.kind)).filter(Record.kind == 3,Record.room == roomid).all()  # 调温
            count2 = mydb.session.query(func.sum(Record.kind)).filter(Record.kind == 2,Record.room == roomid).all()  # 调风
            count3 = mydb.session.query(func.sum(Record.kind)).filter(Record.kind == 1,Record.room == roomid).all()  # 关机
            record = mydb.session.query(Record).filter(Record.room == roomid,Record.time >= stattime,
                                                       Record.time <= endtime, Record.kind < 2).order_by("time").all()
            if (not record):
                count4 = 0
            else:
                timeArray1 = time.strptime(stattime, "%Y-%m-%d %H:%M:%S")
                timeArray2 = time.strptime(endtime, "%Y-%m-%d %H:%M:%S")
                timeStamp1 = int(time.mktime(timeArray1))
                timeStamp2 = int(time.mktime(timeArray2))
                q = 0
                count4 = 0
                for i in record:
                    if (i.kind == 1):
                        timeArray = time.strptime(i.time, "%Y-%m-%d %H:%M:%S")
                        timeStamp = int(time.mktime(timeArray))
                        count4 = count4 + timeStamp - timeStamp1
                        q = 1
                    else:
                        q = 0
                        timeArray1 = time.strptime(i.time, "%Y-%m-%d %H:%M:%S")
                        timeStamp1 = int(time.mktime(timeArray1))
                if (q == 0):
                    count4 = count4 + timeStamp2 - timeStamp1
            result = {'count1': count1, 'count2': count2, 'count3': count3, 'count4': count4}
        except:
            result = {'msg': 'fail'}
    return jsonify(result)


def addRoom(userid, roomid, password, date):
    date = date.strftime("%Y-%m-%d %H:%M:%S")
    room = Room(userid=userid, roomid=roomid, password=password, date=date)
    try:
        mydb.session.add(room)
        mydb.session.commit()
        result = {'msg': 'accept'}
    except:
        # 插入失败的话进行回滚
        mydb.session.rollback()
        mydb.session.flush()
        result = {'msg': '插入失败'}
    return jsonify(result)


# 退房的时候删除相关数据
def deleteRoom(userid, roomid, password):
    try:
        Room.query.filter_by(userid=userid, roomid=roomid, password=password).delete()
        mydb.session.commit()
        result = {'msg': '已删除'}
    except:
        result = {'msg': 'fail'}
    return jsonify(result)


def addUser(uid, password, name, kind):
    user = User(user_id=uid, user_password=password, user_name=name, user_kind=kind)
    try:
        mydb.session.add(user)
        mydb.session.commit()
        result = {'msg': 'accept'}
    except:
        # 插入失败的话进行回滚
        mydb.session.rollback()
        mydb.session.flush()
        result = {'msg': 'fail'}
    return jsonify(result)


def deleteUser(userId):
    try:
        User.query.filter_by(user_id=userId).delete()
        mydb.session.commit()
        result = {'msg': '已删除'}
    except:
        result = {'msg': 'fail'}
    return jsonify(result)


def getUser(userId, password, kind):
    # 也可以先加密password再查询，数据库保存加密后的内容
    user = User.query.filter_by(user_id=userId, user_password=password, user_kind=kind).first()
    if (user is None):
        result = {'msg': '用户名或密码错误'}
    else:
        result = {'username': user.user_name}
    return jsonify(result)


# 包括某个房间空调的请求时间，当前时间，请求时长，风速，费率，费用。
def adddr(room : str, time1 : datetime, time2 : float, time : datetime, speed : str, feerate : float, cost : float):
    with app.app_context():
        time1 = time1.strftime("%Y-%m-%d %H:%M:%S")
        #time2 = time2.strftime("%Y-%m-%d %H:%M:%S") time2是float
        time = time.strftime("%Y-%m-%d %H:%M:%S")
        time2 = float(time2)
        cost = float(cost)
        #print(room,time1,time2,time,speed,feerate,cost)
        #print(type(room), type(time1), type(time2), type(time), type(speed), type(feerate),type(cost))
        bill = Bill(room=room,start_time=time1, during_time=time2,time=time, speed=speed, feerate=feerate, cost=cost)
        try:
            mydb.session.add(bill)
            mydb.session.commit()
            result = {'msg': 'accept'}
            return jsonify(result)
        except:
            # 插入失败的话进行回滚
            mydb.session.rollback()
            mydb.session.flush()
            result = {'msg': '插入失败'}

    return jsonify(result)


def askdr(roomid, end_time):
    with app.app_context():
        end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
        try:
            room = Room.query.filter_by(roomid=roomid).first()
            time = room.date
            bill = mydb.session.query(Bill).filter(Bill.start_time >= time,
                                                   Bill.start_time <= end_time).all()
            if (bill is None):
                result = {'msg': '未查询到数据'}
            else:
                datas = []
                for q in bill:
                    datas.append(
                        {'RoomId': q.room, 'RequestTime': q.start_time, 'RequestDuration': q.time, 'FanSpeed': q.speed, 'FeeRate': q.feerate,
                         'Fee': q.cost})
                return jsonify(data=datas)
        except:
            result = {'msg': 'fail'}
    return jsonify(result)


# 某个房间空调的总费用，入住时间
def asktotalfee(roomid, end_time):
    with app.app_context():
        end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
        try:
            room = Room.query.filter_by(roomid=roomid).first()
            time = room.date
            price = mydb.session.query(func.sum(Bill.cost)).filter(Bill.start_time >= time,
                                                                   Bill.start_time <= end_time).all()[0][0]
            print(price)
            result = {'roomid': roomid, 'price': price, 'time': time}
        except:
            result = {'msg': 'fail'}
    return jsonify(result)


# 详单数目
def askdrnum(roomid, end_time):
    with app.app_context():
        end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
        try:
            room = Room.query.filter_by(roomid=roomid).first()
            start_time = room.date
            count3 = mydb.session.query(func.count(Bill.start_time)).filter(Bill.start_time >= start_time,
                                                                            Bill.start_time <= end_time,
                                                                            Bill.room == roomid).all()
            result = {'num': count3}
        except:
            result = {'msg': 'fail'}
    return jsonify(result)


# 给定时间段内某一个房间的开关次数,空调使用时长,总费用详单数,调温次数,调风次数，应该不用该接口
def getreport111(roomid, start_time, end_time):
    with app.app_context():
        start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
        end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
        try:
            count1 = mydb.session.query(func.sum(Bill.kind)).filter(Bill.start_time >= start_time,
                                                                    Bill.start_time <= end_time, Bill.room == roomid,
                                                                    Bill.kind == 4).all()
            count2 = mydb.session.query(func.sum(Bill.time)).filter(Bill.start_time >= start_time,
                                                                    Bill.start_time <= end_time, Bill.room == roomid).all()
            count3 = mydb.session.query(func.count(Bill.start_time)).filter(Bill.start_time >= start_time,
                                                                            Bill.start_time <= end_time,
                                                                            Bill.room == roomid).all()
            count4 = mydb.session.query(func.sum(Bill.kind)).filter(Bill.start_time >= start_time,
                                                                    Bill.start_time <= end_time, Bill.room == roomid,
                                                                    Bill.kind == 1).all()
            count5 = mydb.session.query(func.sum(Bill.kind)).filter(Bill.start_time >= start_time,
                                                                    Bill.start_time <= end_time, Bill.room == roomid,
                                                                    Bill.kind == 2).all()
            count6 = mydb.session.query(func.sum(Bill.kind)).filter(Bill.start_time >= start_time,
                                                                    Bill.start_time <= end_time, Bill.room == roomid,
                                                                    Bill.kind == 3).all()
            result = {'count1': count1, 'count2': count2, 'count3': count3, 'count4': count4 + count6,
                      'count5': count5 + count6}
        except:
            result = {'msg': 'fail'}
    return jsonify(result)

# if __name__ == '__main__':
#   app.run()
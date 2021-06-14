from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask, jsonify, abort, make_response
import pymysql
from sqlalchemy.sql.functions import count
from sqlalchemy.sql.sqltypes import DateTime
from myglobal import app
# app=Flask(__name__) #创建1个Flask实例
#test
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:xzc19991208@localhost/rg"
#app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:L1nQ1T@ng0xCC@localhost/soft"
# 指定当视图执行完毕后,自动提交数据库操作
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 指定每次执行操作时打印原始的SQL语句
# app.config['SQLALCHEMY_ECHO'] = True
# 防止jsonify出现中文乱码
app.config['JSON_AS_ASCII'] = False
mydb = SQLAlchemy()


class Room(mydb.Model):
    __tablename__ = 'room'
    userid = mydb.Column(mydb.String(255), nullable=False)
    roomid = mydb.Column(mydb.String(255), primary_key=True)
    password = mydb.Column(mydb.String(255), nullable=False)
    date = mydb.Column(mydb.String(255), nullable=False)#入住时间
    def __repr__(self):
        return '<Room %r>' % self.roomid  # = self.func_wxplhdyt()


class User(mydb.Model):
    __tablename__ = 'user'
    user_id = mydb.Column(mydb.String(255), primary_key=True)
    user_password = mydb.Column(mydb.String(255), nullable=False)
    user_name = mydb.Column(mydb.String(255), nullable=False)
    user_kind = mydb.Column(mydb.String(255))    #标识人员身份
    def __repr__(self):
        return '<User %r>' % self.user_id  # = self.func_wxplhdyt()

class Bill(mydb.Model):
    __tablename__ = 'bill'
    room = mydb.Column(mydb.String(255), primary_key=True)
    start_time = mydb.Column(mydb.Integer, primary_key=True)
    end_time = mydb.Column(mydb.Integer, primary_key=True)
    time = mydb.Column(mydb.Integer, primary_key=True)
    tem = mydb.Column(mydb.Float, nullable=False)#温度
    speed = mydb.Column(mydb.Integer, primary_key=True)#风速
    feerate = mydb.Column(mydb.Float, nullable=False)#费率
    cost = mydb.Column(mydb.Float, nullable=False)#这段时间花费
    kind = mydb.Column(mydb.Integer, primary_key=True)#1：调风，2：调温，3：两个都调,4：开关机
    def __repr__(self):
        return '<room %r>' % self.room

mydb.init_app(app)
with app.app_context():
    mydb.init_app(app)
    mydb.create_all()

def addRoom(userid,roomid,password,date):
    room = Room(userid=userid,roomid=roomid,password=password,date=date)
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

#退房的时候删除相关数据
def deleteRoom(userid,roomid,password):
    try:
        Room.query.filter_by(userid=userid,roomid=roomid,password=password).delete()
        mydb.session.commit()
        result = {'msg': '已删除'}
    except:
        result = {'msg': 'fail'}
    return jsonify(result)

def addUser(uid,password,name,kind):
    user = User(user_id=uid,user_password=password,user_name=name,user_kind=kind)
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
def getUser(userId, password):
    # 也可以先加密password再查询，数据库保存加密后的内容
    user = User.query.filter_by(user_id=userId, user_password=password).first()
    if (user is None):
        result = {'msg': '用户名或密码错误'}
    else:
        result = {'username': user.user_name}
    return jsonify(result)

#包括某个房间空调的请求时间，请求时长，风速，费率，费用。
def addbill(room,time1,time2,time,tem,speed,feerate,cost,kind):
    bill = Bill(room=room,start_time=time1,end_time=time2,time=time,tem=tem,speed=speed,feerate=feerate,cost=cost,kind=kind)
    try:
        mydb.session.add(bill)
        mydb.session.commit()
        result = {'msg': 'accept'}
    except:
        # 插入失败的话进行回滚
        mydb.session.rollback()
        mydb.session.flush()
        result = {'msg': '插入失败'}
    return jsonify(result)
def getbill(roomid,end_time):
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
                datas.append({'room': q.room,'start_time':q.start_time,'time':q.time,'speed':q.speed,'feerate':q.feerate,'cost':q.cost})
            return jsonify(data=datas)    
    except:
        result={'msg':'fail'}
    return result
#某个房间空调的总费用，入住时间
def getbills(roomid,end_time):
    try:
        room = Room.query.filter_by(roomid=roomid).first()
        time = room.date
        price = mydb.session.query(func.sum(Bill.cost)).filter(Bill.start_time >= time,
                                               Bill.start_time <= end_time).all()
        result = {'roomid': roomid,'price':price,'time':time}
    except:
        result = {'msg':'fail'}
    return jsonify(result)
#给定时间段内某一个房间的开关次数,空调使用时长,总费用详单数,调温次数,调风次数
def getreport(roomid,start_time,end_time):
    try:
        count1 = mydb.session.query(func.sum(Bill.kind)).filter(Bill.start_time >= start_time,
                                               Bill.start_time <= end_time,Bill.room == roomid,Bill.kind == 4).all()
        count2 = mydb.session.query(func.sum(Bill.time)).filter(Bill.start_time >= start_time,
                                               Bill.start_time <= end_time,Bill.room == roomid).all()
        count3 = mydb.session.query(func.count(Bill.start_time)).filter(Bill.start_time >= start_time,
                                               Bill.start_time <= end_time,Bill.room == roomid).all()
        count4 = mydb.session.query(func.sum(Bill.kind)).filter(Bill.start_time >= start_time,
                                               Bill.start_time <= end_time,Bill.room == roomid,Bill.kind == 1).all()
        count5 = mydb.session.query(func.sum(Bill.kind)).filter(Bill.start_time >= start_time,
                                               Bill.start_time <= end_time,Bill.room == roomid,Bill.kind == 2).all()
        count6 = mydb.session.query(func.sum(Bill.kind)).filter(Bill.start_time >= start_time,
                                               Bill.start_time <= end_time,Bill.room == roomid,Bill.kind == 3).all()                                                                                   
        result = {'count1':count1,'count2':count2,'count3':count3,'count4':count4+count6,'count5':count5+count6}
    except:
        result={'msg':'fail'}    
    return jsonify(result)
    
# if __name__ == '__main__':
#   app.run()

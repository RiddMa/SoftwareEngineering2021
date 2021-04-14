from flask import Flask
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, abort, make_response
import pymysql
app=Flask(__name__) #创建1个Flask实例

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:xzc19991208@localhost/rg"
#指定当视图执行完毕后,自动提交数据库操作
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#指定每次执行操作时打印原始的SQL语句
#app.config['SQLALCHEMY_ECHO'] = True
#防止jsonify出现中文乱码
app.config['JSON_AS_ASCII'] = False
mydb = SQLAlchemy()

class Card(mydb.Model):
  __tablename__ = 'card'
  name = mydb.Column(mydb.String(255), primary_key=True)
  roomid = mydb.Column(mydb.String(255), nullable=False)
  password = mydb.Column(mydb.String(255), nullable=False)
  def __repr__(self):
    return '<Card %r>' % self.roomid #= self.func_wxplhdyt()
class User(mydb.Model):
  __tablename__ = 'user'
  user_id = mydb.Column(mydb.String(255), primary_key=True)
  user_password = mydb.Column(mydb.String(255), nullable=False)
  user_name = mydb.Column(mydb.String(255), nullable=False)
  user_kind = mydb.Column(mydb.String(255))
  def __repr__(self):
    return '<User %r>' % self.user_id #= self.func_wxplhdyt()
class Client(mydb.Model):
  __tablename__ = 'client'
  room_id = mydb.Column(mydb.String(255), primary_key=True)
  client_name = mydb.Column(mydb.String(255), nullable=False)
  client_passward = mydb.Column(mydb.String(255), nullable=False)
  client_idcard = mydb.Column(mydb.String(255), nullable=True)
  client_phonenumber = mydb.Column(mydb.String(255), nullable=True)
  def __repr__(self):
    return '<room %r>' % self.room_id   
class Bill(mydb.Model):
  __tablename__ = 'bill'
  room = mydb.Column(mydb.String(255), primary_key=True)
  start_time = mydb.Column(mydb.String(255), primary_key=True)
  end_time = mydb.Column(mydb.String(255), primary_key=True)
  cost = mydb.Column(mydb.Integer, nullable=False)
  def __repr__(self):
    return '<room %r>' % self.room
mydb.init_app(app)
with app.app_context():
  mydb.init_app(app)
  mydb.create_all()
def getCard(roomid,password):
  card = Card.query.filter_by(roomid=roomid,password=password).first()
  if(card is None):
    result = {'msg': '房间号或或密码错误'}
  else:
    result = {'name': card.name}
  return jsonify(result)
def getClient(roomid,password):
  client = Client.query.filter_by(room_id=roomid,client_passward=passward).first()
  if (user is None):
    result = {'msg': '用户名或密码错误'}
  else:
    result = {'msg': 'accept!' }
  return jsonify(result)
def getClients():
  data = Client.query.all()
  datas = []
  for q in data:
    datas.append({'room_id': q.romm_id, 'client_name': q.client_name})
  return jsonify(data=datas)
#@app.route('/') 感觉用不到路由
def getUser(userId,password):
  #也可以先加密passward再查询，数据库保存加密后的内容
  user = User.query.filter_by(user_id=userId,user_passward=passward).first()
  if (user is None):
    result = {'msg': '用户名或密码错误'}
  else:
    result = {'username': user.user_name}
  return jsonify(result)

def getBill(roomid,starttime,endtime):
  bill= mydb.session.query(Bill).filter(Bill.room==roomId,Bill.start_time<=starttime,Bill.end_time<=endtime).all()
  if (bill is None):
    result = {'msg': '未查询到数据'}
  else:
    datas = []
    for q in bill:
      datas.append({'rid': q.room,'start_time' : q.start_time,'end_time' : q.end_time,'price' : q.cost})
    return jsonify(data=datas)
  return 

def addBill(room,start_time,endtime,cost):
  bill = Bill(room=room,start_time=time,end_time=endtime,cost=cost)
  try:
    mydb.session.add(bill)
    mydb.session.commit()
    result={'msg': 'accept'}
  except:
    #插入失败的话进行回滚
    mydb.session.rollback()
    mydb.session.flush()
    result={'msg': '插入失败'}
  return jsonify(result)
def addClient():
  client = Client() 
  try:
    mydb.session.add(user)
    mydb.session.commit()
    result={'msg': 'accept'}
  except:
    #插入失败的话进行回滚
    mydb.session.rollback()
    mydb.session.flush()
    result={'msg': '插入失败'}
  return jsonify(result)
def addUser():
  user = User()
  try:
    mydb.session.add(client)
    mydb.session.commit()
    result={'msg': 'accept'}
  except:
    #插入失败的话进行回滚
    mydb.session.rollback()
    mydb.session.flush()
    result={'msg': 'fail'}
  return jsonify(result)
def updateUser(userId,name,passward,kind):#改变用户名,密码，kind
  try:
    user = User.query.filter_by(user_id=userId).first()
    if (user is None):
      result = {'msg': '找不到要修改的记录'}
      return jsonify(data=result)
    else:
      user.user_name = name
      user.user_passward=passward
      user.user_kind = kind
      mydb.session.commit()
      result = {'msg': 'accept'}
  except:
    mydb.session.rollback() # 回滚
    mydb.session.flush() # 重置
    result = {'msg': 'fail'}
  return jsonify(result)
def deleteUser(userId):
  User.query.filter_by(user_id=userId).delete()
  mydb.session.commit()
  result = {'msg': '已删除'}
  return jsonify(result)
def deleteClient(roomid):
  Client.query.filter_by(room_id=roomid).delete()
  mydb.session.commit()
  result = {'msg': '已删除'}
  return jsonify(result)
def deleteBill(roomid,starttime,endtime):
  Bill.query.filter_by(room_id=roomid,start_time=starttime,end_time=endtime).delete()
  mydb.session.commit()
  result = {'msg': '已删除'}
  return jsonify(result)
def deletecard(name,roomid,password):
  Card.query.filter_by(name=name,roomid=roomid,password=password).delete()
  mydb.session.commit()
  result = {'msg': '已删除'}
  return jsonify(result)
if __name__ == '__main__':
  app.run()     
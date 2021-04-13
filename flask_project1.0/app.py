from flask import Flask, request, jsonify
import json
from flask_cors import CORS

from model import Admin, Reception, User

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello World!'


#管理员模块
@app.route('/admin/login', methods=['POST'])
def admin_login():
    form = request.get_json()
    username = form['username']
    password = form['password']

    res = dict()
    error_code, admin = Admin.get_admin(username, password)
    if error_code == 1:
        res['error_code'] = 1
    else:
        res['error_code'] = 0
        res['data'] = dict()
        res['data']['uid'] = admin.id
        res['data']['username'] = admin.username
        res['data']['token'] = admin.token

    return jsonify(res)

    # return jsonify({
    #                     "error_code": 0,
    #                     "data": {
    #                         "uid": "1",
    #                         "username": "liming",
    #                         "token": "XXXXXX"
    #                     }
    #                 })


@app.route('/admin/createreport', methods=['POST'])
def create_report():
    form = request.get_json()
    time = form['timestamp']

    error_code, room_states = Admin.get_report(time)
    res = dict()
    if error_code == 1:
        res['error_code'] = 1
    else:
        res['error_code'] = 0
        res['data'] = room_states

    return jsonify(res)
    # return jsonify({
    #                     "error_code": 0,
    #                     "data": [
    #                         {
    #                             "rid": "101",
    #                             "state": "1",
    #                             "temp":"26",
    #                             "mode":"1",
    #                             "discount":"0.8",
    #                         }
    #                     ]
    #                 })


@app.route('/admin/createwaterbills', methods=['POST'])
def create_water_bills():
    # form = request.get_json()
    # date = form['date']
    #
    # return {
    #         "error_code": 0,
    #         "data":[
    #                 {
    #                     "rid":"101",
    #                     "time":"2021-04-03 23:42:50",
    #                     "account":"87.60"
    #                 }
    #             ]
    #         }
    return jsonify({})


@app.route('/admin/discount', methods=['POST'])
def admin_discount():
    form = request.get_json()
    rid = form['rid']
    discount = form['discount']

    error_code = Admin.set_discount(rid, discount)

    return jsonify({"error_code": error_code})


@app.route('/admin/centerturnonoff', methods=['POST'])
def center_switch():
    form = request.get_json()
    state = form['state']

    error_code = Admin.center_turn_on_off(state)

    return jsonify({'error': error_code})


#前台模块
@app.route('/reception/signin', methods=['POST'])
def reception_signin():
    form = request.get_json()
    ph_num = form['phonenumber']

    error_code, card = Reception.get_card(ph_num)
    res = dict()
    if error_code == 1:
        res['error_code'] = 1
    else:
        res['error_code'] = 0
        res['data'] = dict()
        res['data']['name'] = card.username
        res['data']['rid'] = card.rid
        res['data']['password'] = card.password

    return jsonify(res)
    # return jsonify({
    #                     "error_code": 0,
    #                     "data": {
    #                         "name": "liming",
    #                         "rid": "101",
    #                         "password":"26"
    #                      }
    #                 })


@app.route('/reception/logout')
def reception_logout():
    form = request.get_json()
    rid = form['rid']

    error_code, duration, price = Reception.get_total_cost(rid)

    return jsonify({
                        "error_code": error_code,
                        "data": {
                                "duration": duration,
                                "price": price
                            }
                    })


#顾客模块
@app.route('/user/turnonoff')
def user_turn_on_off():
    form = request.get_json()
    rid = form['rid']
    state = form['state']

    error_code = User.turn_on_off(rid, state)

    return jsonify({'error': error_code})


@app.route('/user/settemp')
def user_set_temp():
    form = request.get_json()
    rid = form['rid']
    temp = form['settemp']

    error_code = User.set_temp(rid, temp)

    return jsonify({'error': error_code})


@app.route('/user/setmode')
def user_set_mode():
    form = request.get_json()
    rid = form['rid']
    mode = form['setmode']

    error_code = User.set_mode(rid, mode)

    return jsonify({'error': error_code})


@app.route('/user/showcost')
def user_show_cost():
    form = request.get_json()
    rid = form['rid']

    error_code, cost, onoff = User.show_cost(rid)
    res = dict()
    if error_code == 1:
        res['error_code'] = 1
    else:
        res['error_code'] = 0
        res['data'] = dict()
        res['data']['onoff'] = onoff
        res['data']['cost'] = cost

    return jsonify(res)
    # return jsonify({
    #                     "error_code": 0,
    #                     "data": {
    #                         "onoff": "1",
    #                         "cost":"99.43"
    #                     }
    #                 })


if __name__ == '__main__':
    app.run()

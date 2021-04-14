from flask import Flask, request, jsonify, make_response, sessions
import json
from flask_cors import CORS

from model import Admin, User

app = Flask(__name__)
CORS(app)


# admin_tokens = set()
# user_tokens = set()
# admin_tokens.add('XXXXXX')
# user_tokens.add('XXXXXX')

# def set_token(is_admin, token):
#     if is_admin == True:
#         admin_tokens.add(token)
#     else:
#         user_tokens.add(token)
#
#
# def verify_token(is_admin, token):
#     if is_admin == True:
#         return token in admin_tokens
#     else:
#         return token in user_tokens


@app.route('/')
def hello_world():
    return 'Hello World!'


#管理员模块
@app.route('/admin/login', methods=['POST'])
def admin_login():
    form = request.get_json()
    username = form['username']
    password = form['password']

    res = map()
    error_code, admin = Admin.get_admin(username, password)
    if error_code == 1:
        res['error_code'] = 1
    else:
        res['error_code'] = 0
        res['data'] = map()
        res['data']['uid'] = admin.id
        res['data']['username'] = admin.name
    #     res['data']['token'] = admin.token
    #     set_token(True, admin.token)
    #
    #
    return jsonify(res)

    # resp = make_response(jsonify({
    #                     "error_code": 0,
    #                     "data": {
    #                         "uid": "1",
    #                         "username": "liming"
    #                     }
    #                 }))
    # resp.set_cookie('token', 'XXXXXX', max_age=3600, path='/')
    #
    # return resp


@app.route('/admin/createreport', methods=['POST'])
def create_report():
    form = request.get_json()
    time = form['timestamp']
    token = request.cookies.get('token')

    # if not verify_token(True, token):
    #     return jsonify({'error_code' : 1})

    error_code, room_states = Admin.get_report(time)
    res = map()
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
    #                             "discount":"0.8"
    #                         },
    #                         {
    #                             "rid": "102",
    #                             "state": "1",
    #                             "temp": "20",
    #                             "mode": "1",
    #                             "discount": "0.75"
    #                         }
    #                     ]
    #                 })


# @app.route('/admin/createwaterbills', methods=['POST'])
# def create_water_bills():
#     # form = request.get_json()
#     # date = form['date']
#     #
#     # return {
#     #         "error_code": 0,
#     #         "data":[
#     #                 {
#     #                     "rid":"101",
#     #                     "time":"2021-04-03 23:42:50",
#     #                     "account":"87.60"
#     #                 }
#     #             ]
#     #         }
#     return jsonify({})


@app.route('/admin/discount', methods=['POST'])
def admin_discount():
    form = request.get_json()
    rid = form['rid']
    discount = form['discount']
    # token = request.cookies.get('token')

    # if not verify_token(True, token):
    #     return jsonify({'error_code' : 1})

    error_code = Admin.set_discount(rid, discount)

    return jsonify({"error_code": error_code})


@app.route('/admin/centerturnonoff', methods=['POST'])
def center_switch():
    form = request.get_json()
    state = form['state']
    # token = request.cookies.get('token')

    # if not verify_token(True, token):
    #     return jsonify({'error_code': 1})

    error_code = Admin.center_turn_on_off(state)

    return jsonify({'error': error_code})


#前台模块
# @app.route('/reception/signin', methods=['POST'])
# def reception_signin():
#     form = request.get_json()
#     ph_num = form['phonenumber']
#
#     # error_code, card = Reception.get_card(ph_num)
#     # res = map()
#     # if error_code == 1:
#     #     res['error_code'] = 1
#     # else:
#     #     res['error_code'] = 0
#     #     res['data'] = map()
#     #     res['data']['name'] = card.username
#     #     res['data']['rid'] = card.rid
#     #     res['data']['password'] = card.password
#     #
#     # return jsonify(res)
#     return jsonify({
#                         "error_code": 0,
#                         "data": {
#                             "name": "liming",
#                             "rid": "101",
#                             "password":"26"
#                          }
#                     })
#
#
# @app.route('/reception/logout', methods=['POST'])
# def reception_logout():
#     form = request.get_json()
#     rid = form['rid']
#
#     # error_code, duration, price = Reception.get_total_cost(rid)
#
#     return jsonify({
#                         "error_code": 0,
#                         "data": {
#                                 "duration": 0,
#                                 "price": 0
#                             }
#                     })


#顾客模块
@app.route('/user/checkin', methods=['POST'])
def enter_room():
    form = request.get_json()
    rid = form['rid']
    password = form['password']


    error_code, user= User.user_login()
    if error_code == 1:
        return jsonify({'error_code' : 1})

    res = map()
    res['uid'] = user.id
    res['username'] = user.name
    # res['token'] = token
    return jsonify({'error_code': error_code, 'data': res})

    # resp = make_response(jsonify({
    #             "error_code": 0,
    #             "data": {
    #               "uid": "1",
    #               "username": "liming"
    #             }
    #         }))

    # resp.set_cookie('token', 'XXXXXX', path= '/')


    # return resp


@app.route('/user/turnonoff', methods=['POST'])
def user_turn_on_off():
    form = request.get_json()
    rid = form['rid']
    state = form['state']
    # token = request.cookies.get('token')

    # if not verify_token(False, token):
    #     return jsonify({'error_code': 1})

    error_code = User.turn_on_off(rid, state)

    return jsonify({'error_code': error_code})


@app.route('/user/settemp', methods=['POST'])
def user_set_temp():
    form = request.get_json()
    rid = form['rid']
    temp = form['settemp']
    # token = request.cookies.get('token')

    # if not verify_token(False, token):
    #     return jsonify({'error_code': 1})

    error_code = User.set_temp(rid, temp)

    return jsonify({'error_code': error_code})


@app.route('/user/setmode', methods=['POST'])
def user_set_mode():
    form = request.get_json()
    rid = form['rid']
    mode = form['setmode']
    # token = request.cookies.get('token')

    # if not verify_token(False, token):
    #     return jsonify({'error_code': 1})

    error_code = User.set_mode(rid, mode)

    return jsonify({'error_code': error_code})


@app.route('/user/showcost', methods=['POST'])
def user_show_cost():
    form = request.get_json()
    rid = form['rid']
    # token = request.cookies.get('token')

    # if not verify_token(False, token):
    #     return jsonify({'error_code': 1})

    error_code, cost, onoff = User.show_cost(rid)
    res = map()
    if error_code == 1:
        res['error_code'] = 1
    else:
        res['error_code'] = 0
        res['data'] = map()
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

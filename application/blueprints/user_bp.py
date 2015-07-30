from flask import Blueprint, session, request, jsonify,render_template
from bson.objectid import ObjectId
from bson.json_util import loads

from ..models.user import User
from . import is_login

user_bp= Blueprint('user_bp', __name__)

@user_bp.route('/login', methods = ['POST'])
def login():
    user_phone = request.form['phone']
    user = User.get_user_by_phone(user_phone)
    if user != 'null' and loads(user)['password']==request.form['password']:
        session['phone'] = user_phone
        data = {
            'status':200,
            'data': 'success'
        }
        resp = jsonify(data)
        # resp.status_code = 200
    else:
        data = {
            'status':403,
            'data': 'fail'
        }
        resp = jsonify(data)
        # resp.status_code = 403
    return resp

@user_bp.route('/logintest')
def testlogin():
    return render_template('form.html')

@user_bp.route('/registertest')
def registertest():
    return render_template('registertest.html')

@user_bp.route('/collect-user-test')
def collect_user_test():
    return render_template('collect-user-test.html')

@user_bp.route('/logout')
def logout():
    if is_login():
        session.pop('phone', None)
        data = {
            'status':200,
            'data':'success'
        }
        resp = jsonify(data)
        # resp.status_code = 200
        return resp
    else:
        data = {
            'status':401,
            'data':'user not log in'
        }
        resp = jsonify(data)
        # resp.status_code = 403
        return resp

@user_bp.route('/register', methods = ['POST'])
def register():
    user_phone = request.form['phone']
    user_password = request.form['password']
    user_avatar = request.form['avatar']
    print user_phone, user_password, user_avatar
    if User.get_user_by_phone(user_phone) != 'null':
        data = {
            'status':403,
            'data':'user exit!'
        }
        resp = jsonify(data)
        # resp.status_code = 403
    else:
        r_user = User(user_phone, user_password, user_avatar)
        result = User.insert_user(r_user) 
        if not result:
            data = {
                'status':200,
                'data':'success'
            }
            resp = jsonify(data)
            # resp.status_code = 200
        else:
            data = {
                'status':500,
                'data':'create user fail'
            }
            resp = jsonify(data)
            # resp.status_code = 500
    return resp



@user_bp.route('/collect-user', methods = ['POST'])
def collect_user():
    if is_login():
        user = User.get_user_by_phone(session['phone'])
        user_id = loads(user)['_id']
        collect_user_id = ObjectId(request.form['user_id'])
        result = User.add_focus_user(user_id, collect_user_id)
        if result == '':
            data = {
                'status':200,
                'data':'success'
            }
            return jsonify(data)
        else:
            data = {
                'status':403,
                'data':result
            }
            return jsonify(data)
    else:
        return jsonify(
            {
                'status':401,
                'data':'user not log in'
            })


@user_bp.route('/collect-plane')
def collect_plane():
    if is_login():
        user = User.get_user_by_phone(session['phone'])
        user_id = loads(user)['_id']
        collect_story_id = ObjectId(request.form['story_id'])
        result = User.add_focus_story(user_id, collect_story_id)
        if result == '':
            data = {
                'status':200,
                'data':'success'
            }
            return jsonify(data)
        else:
            data = {
                'status':403,
                'data':result
            }
            return jsonify(data)
    else:
        return jsonify(
            {
                'status':401,
                'data':'user not log in'
            })


@user_bp.route('/draft')
def draft():
    return ""

#-*- coding: UTF-8 -*- 

from flask import Blueprint, session, request, jsonify,render_template
from bson.objectid import ObjectId
from bson.json_util import loads,dumps
import json

from ..models.user import User
from ..models.story import Story
from . import is_login, convert_id

user_bp= Blueprint('user_bp', __name__)

@user_bp.route('/login', methods = ['POST'])
def login():
    # request_json = json.loads(request.data)
    user_phone = json.loads(request.data).get('phone')
    user_password = json.loads(request.data).get('password')
    user_token = json.loads(request.data).get('token')
    if user_token != None:
        user = User.get_user_by_token(user_token)

        if user != 'null':
            session['token'] = user_token
            return jsonify({
                    'status':200,
                    'data':'success'
                })
        else:
            new_user = User("", "", "", user_token)
            if User.insert_user(new_user) == "":
                session['token'] = user_token
                return jsonify({
                        'status':200,
                        'data':'token register user success'
                    })
            return jsonify({
                    'status':403,
                    'data':'fail'
                })
    # user_phone = request_json['phone']
    # user_password = request_json['password']
    user = User.get_user_by_phone(user_phone)
    if user != 'null' and loads(user)['password']==user_password:
        session['phone'] = user_phone
        data = {
            'status':200,
            'data': 'success'
        }
        resp = jsonify(data)
    else:
        data = {
            'status':403,
            'data': 'fail'
        }
        resp = jsonify(data)
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
        session.pop('token', None)
        data = {
            'status':200,
            'data':'success'
        }
        resp = jsonify(data)
        return resp
    else:
        data = {
            'status':401,
            'data':'user not log in'
        }
        resp = jsonify(data)
        return resp

@user_bp.route('/register', methods = ['POST'])
def register():
    user_phone = json.loads(request.data)['phone']
    user_password = json.loads(request.data)['password']
    user_avatar = json.loads(request.data)['avatar']
    if User.get_user_by_phone(user_phone) != 'null':
        data = {
            'status':403,
            'data':'user exit!'
        }
        resp = jsonify(data)
    else:
        r_user = User(user_phone, user_password, user_avatar)
        result = User.insert_user(r_user) 
        if not result:
            data = {
                'status':200,
                'data':'success'
            }
            resp = jsonify(data)
        else:
            data = {
                'status':500,
                'data':'create user fail'
            }
            resp = jsonify(data)
    return resp



@user_bp.route('/collect-user', methods = ['POST'])
def collect_user():
    if is_login():
        user = User.get_user_by_phone(session['phone'])
        user_id = loads(user)['_id']
        # collect_user_id = ObjectId(json.loads(request.data)['user_id'])
        collect_user_id = ObjectId(json.loads(request.data)['user_id'])
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


@user_bp.route('/collect-plane', methods = ['POST'])
def collect_plane():
    if is_login():
        user = User.get_user_by_phone(session['phone'])
        user_id = loads(user)['_id']
        # collect_story_id = ObjectId(json.loads(request.data)['story_id'])
        collect_story_id = ObjectId(json.loads(request.data)['story_id'])
        story = Story.get_story_by_id(collect_story_id)
        if story == 'null':
            return jsonify({
                    'status':403,
                    'data':'invalid story id'
                })
        story = loads(story)
        story['total_collections'] += 1
        result = User.add_focus_story(user_id, collect_story_id)
        if result == '':
            result_story = Story.update_story(story)
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


# # @user_bp.route('/draft')
# # def draft():
# #     return ""
# @user_bp.route('/test')
# def test():
#     return Story.get_story_by_id(ObjectId("55b8b9ddf5888d3ac24de210"))

@user_bp.route('/show-focus-users')
def show_foucs_users():
    if not is_login():
        return jsonify({
                'status':401,
                'data':'user not log in'
            })
    user = User.get_user_by_phone(session['phone'])
    focus_users = loads(user)['focus_users']
    if not focus_users:
        return jsonify({
                'status':200,
                'data':""
            })
    else:
        return_users = []
        for single_user_id in focus_users:
            single_user = User.get_user(single_user_id)
            if single_user != 'null':
                single_user = loads(single_user)
                del single_user['focus_stories']
                del single_user['focus_users']
                del single_user['phone']
                del single_user['password']
                return_users.append(single_user)
        return jsonify({
                'status':200,
                'data':convert_id(return_users)
            })


@user_bp.route('/show-focus-stories')
def show_foucs_stories():
    if not is_login():
        return jsonify({
                'status':401,
                'data':'user not log in'
            })
    user = User.get_user_by_phone(session['phone'])
    focus_stories = loads(user)['focus_stories']
    if not focus_stories:
        return jsonify({
                'status':200,
                'data':""
            })
    else:
        return_stories = []
        for single_story_id in focus_stories:
            single_story = Story.get_story_by_id(single_story_id)
            if single_story != 'null':
                single_story = loads(single_story)
                del single_story['paragraph_ids']
                del single_story['current_owner']
                return_stories.append(single_story)
        return jsonify({
                'status':200,
                'data':convert_id(return_stories)
            })
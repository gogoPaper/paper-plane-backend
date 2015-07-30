from flask import Blueprint, session, request, jsonify
from bson.json_util import loads,dumps

def is_login():
    if 'phone' in session:
        return True
    else:
        return False

def convert_id(data):
    if isinstance(data, list):
        for single_data in data:
            single_data['_id'] = str(single_data['_id'])
        return dumps(data)
    data['_id'] = str(data['_id'])
    return dumps(data)
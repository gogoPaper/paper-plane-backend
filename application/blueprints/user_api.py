from flask import Blueprint

from ..models.message import Message
from ..utils.db import db
user_api = Blueprint('user_api', __name__)

@user_api.route('/')
def index():
    return 'Hello World!'

@user_api.route('/testdb')
def testdb():
    return ""
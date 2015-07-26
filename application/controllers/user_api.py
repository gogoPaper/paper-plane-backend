from flask import Blueprint

from ..models.paragraph import paragraph

user_api = Blueprint('user_api', __name__)

@user_api.route('/')
def index():
    return 'Hello World!'

@user_api.route('/testdb')
def testdb():
    para = paragraph()
    return str(para.test())

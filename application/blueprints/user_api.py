from flask import Blueprint
from bson.objectid import ObjectId
from bson.json_util import loads

from ..models.message import Message
from ..models.paragraph import Paragraph
from ..models.story import Story
from ..models.user import User

from ..utils.db import db
user_api = Blueprint('user_api', __name__)

@user_api.route('/')
def index():
    return 'Hello World!'

@user_api.route('/testdb')
def testdb():
    # u_paragraph = loads(Paragraph.get_paragraph(ObjectId("55b6dbcbf5888d1ada082f8c")))
    # return Paragraph.incre_favours(u_paragraph['_id'])

    # story = Story('test', "123", "carloswei")


    # u_story = loads(Story.get_story_by_id(ObjectId("55b6e573f5888d2fad493f61")))
    # u_story['current_owner'] = "carlosweiV2"
    # return Story.update_story(u_story)

    # user = User("15521286293", "19941995", "carloswei", "/ser/dfe")
    # return User.get_user_by_phone("15521286293")

    # u_user = loads(User.get_user(ObjectId("55b6f05cf5888d30bcf88de8")))
    # u_user['nickname'] = "carlosweiV2"
    # return User.update_user(u_user)
    # return Paragraph.toggle_user_favours(ObjectId("55b72f6bf5888d36f0634bb6"), "testid")
    return "test"
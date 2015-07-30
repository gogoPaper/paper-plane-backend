from flask import Blueprint, session, request, jsonify,render_template
from bson.objectid import ObjectId
from bson.json_util import loads
from datetime import datetime

from ..models.message import Message
from ..models.paragraph import Paragraph
from ..models.story import Story
from ..models.user import User

from . import convert_id, is_login
plane_bp= Blueprint('plane_bp', __name__)

@plane_bp.route('/')
def index():
    story_id = request.args.get('story_id', '')
    if story_id == '':
        return jsonify( {
            'status':403,
            'data':''
        })

    story = Story.get_story_by_id(ObjectId(story_id))
    if story != 'null':
        story = loads(story)
        del story['paragraph_ids']
        del story['current_owner']
        data = {
            'status':200,
            'data':convert_id(story)
        }
    else:
        data = {
            'status':403,
            'data':'the story does not exist'
        }
    return jsonify(data)


@plane_bp.route('/flytest')
def flytest():
    return render_template('flytest.html')

@plane_bp.route('/fly', methods = ['POST'])
def fly():
    if not is_login():
        return jsonify({
            'status':403,
            'data':'user not log in'
            })
    story_id = request.form['story_id']
    title = request.form['title']
    content = request.form['content']
    user_phone =  session['phone']
    user_id = loads(User.get_user_by_phone(user_phone))['_id']

    if content == "":
        return jsonify(
            {
                'status':403,
                'data':"empty content"
            })
    if story_id == '':
        story = Story(title).get_as_json()
        new_story_id = story['_id']
        first_paragraph = Paragraph(user_id, new_story_id, content).get_as_json()
        story['paragraph_ids'].append(first_paragraph['_id'])
        if Story.insert_story(story) == "" and Paragraph.insert_paragraph(first_paragraph)=="":
            return jsonify({
                    'status':200,
                    'data':'success'
                })
        else:
            return jsonify({
                    'status':403,
                    'data':'fail to create a plane'
                })
    else:
        story = Story.get_story_by_id(ObjectId(story_id))
        if story == 'null':
            return jsonify({
                    'status':403,
                    'data':'invalid story id'
                })
        else:
            story = loads(story)
            story['status'] = 0
            story['current_owner'] = ""
            new_paragraph = Paragraph(user_id, ObjectId(story_id), content).get_as_json()
            story['paragraph_ids'].append(new_paragraph['_id'])
            if Story.update_story(story) == "" and Paragraph.insert_paragraph(new_paragraph) == "":
                return jsonify({
                        'status':200,
                        'data':'success'
                    })
            else:
                return jsonify({
                        'status':403,
                        'data':'fail to continue a plane'
                    })


@plane_bp.route('/hot')
def hot():
    amount = request.args.get('amount', '')
    offset = request.args.get('offset', '')
    if amount == '' or offset == '':
        return jsonify({
                'status':403,
                'data':'invalid parameters'
            })
    result = Story.get_story_by_fields(int(offset), int(amount))
    if result == 'null':
        return jsonify({
                'status':200,
                'data':''
            })
    else:
        result = loads(result)
        for r in result:
            del r['paragraph_ids']
            del r['current_owner']
        return jsonify({
                'status':200,
                'data':convert_id(result)#paragraph_id is still not convert
            })

@plane_bp.route("/occupy")
def occupy():
    
    

@plane_bp.route("/throw")
def throw_plane():
    return ""


#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from bson.json_util import dumps, loads

from application.models.message import Message
from application.models.user import User
from application.models.story import Story
from application.models.paragraph import Paragraph
from application.utils.db import db
import application

"""
class MessageTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        collection = db['message']
        collection.remove({})

    def test_get_as_json(self):
        sender = 1
        content = "test"
        message = Message(sender, content)
        msg_dict = message.get_as_json()
        self.assertEquals(1, msg_dict['sender'])
        self.assertEquals("test", msg_dict['content'])

    def test_insert_message(self):
        sender = 1
        content = "test"
        message = Message(sender, content)
        self.assertEquals("", Message.insert_message(message))

    def test_get_one_message(self):
        sender = 1
        content = "test"
        message = Message(sender, content)
        Message.insert_message(message)
        # self.assertEquals(message.get_as_json(), Message.get_message(message._id))
        # print type(Message.get_message(message._id))
        # users = loads(User.get_user(ObjectId("55b6f05cf5888d30bcf88de8")))
        actual_msg = loads(Message.get_message(message._id))
        self.assertEquals(message.__dict__, actual_msg)

    def test_get_all_message(self):
        msg_num = 3
        # 将所有message用dumps转为str放到set中
        msg_id_set = set()
        for i in range(msg_num):
            sender = i
            content = "content of %d" % i
            message = Message(sender, content)
            msg_id_set.add(message._id)
            Message.insert_message(message)
        actual_msg_list = loads(Message.get_message())
        actual_msg_id_set = set()
        # 取出后也全部转str放到set中
        for actual_msg in actual_msg_list:
            actual_msg_id_set.add(actual_msg['_id'])
        # 只比较set判断是否一致
        self.assertEquals(msg_id_set, actual_msg_id_set)

    def test_get_message_by_sender(self):
        msg_num = 3
        sender = 1
        msg_id_set = set()
        for i in range(msg_num):
            content = "content of %d" % i
            message = Message(sender, content)
            msg_id_set.add(dumps(message.__dict__))
            Message.insert_message(message)
        actual_msg_list = loads(Message.get_message_by_sender(sender))
        actual_msg_id_set = set()
        for actual_msg in actual_msg_list:
            actual_msg_id_set.add(dumps(actual_msg))
        self.assertEquals(msg_id_set, actual_msg_id_set)

    def test_update_message(self):
        sender = 1
        content = "test"
        u_content = "test updated"
        message = Message(sender, content)
        Message.insert_message(message)
        # 需要先从Message中get出来再修改
        msg_origin = loads(Message.get_message(message._id))
        msg_origin['content'] = u_content
        self.assertEquals("", Message.update_message(msg_origin))
        self.assertEquals(dumps(msg_origin), Message.get_message(message._id))

    def test_delete_message(self):
        sender = 1
        content = "test"
        message = Message(sender, content)
        Message.insert_message(message)
        self.assertEquals("", Message.delete_message(message._id))
        self.assertEquals("null", Message.get_message(message._id))

class UserTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        collection = db['user']
        collection.remove({})

    def test_get_as_json(self):
        phone = "123456"
        password = "123456"
        nickname = "nick"
        avatar = "avatar"
        user = User(phone, password, nickname, avatar)
        user_dict = user.get_as_json()
        self.assertEquals(phone, user_dict['phone'])
        self.assertEquals(password, user_dict['password'])
        self.assertEquals(nickname, user_dict['nickname'])
        self.assertEquals(avatar, user_dict['avatar'])

    def test_insert_user(self):
        phone = "123456"
        password = "123456"
        nickname = "nick"
        avatar = "avatar"
        user = User(phone, password, nickname, avatar)
        self.assertEquals("", User.insert_user(user))

    def test_get_one_user(self):
        phone = "123456"
        password = "123456"
        nickname = "nick"
        avatar = "avatar"
        user = User(phone, password, nickname, avatar)
        User.insert_user(user)
        self.assertEquals(user.__dict__, loads(User.get_user(user._id)))

    def test_get_all_user(self):
        user_num = 3
        user_id_set = set()
        for i in range(user_num):
            phone = str(i)
            password = str(i)
            nickname = str(i)
            avatar = str(i)
            user = User(phone, password, nickname, avatar)
            user_id_set.add(user._id)
            User.insert_user(user)
        actual_user_list = loads(User.get_user())
        actual_user_id_set = set()
        for actual_user in actual_user_list:
            actual_user_id_set.add(actual_user['_id'])
        self.assertEquals(user_id_set, actual_user_id_set)


    def test_get_user_by_phone(self):
        phone = "123456"
        password = "123456"
        nickname = "nick"
        avatar = "avatar"
        user = User(phone, password, nickname, avatar)
        User.insert_user(user)
        user_dict = loads(User.get_user_by_phone(phone))
        self.assertEquals(user._id, user_dict['_id'])
        self.assertEquals(phone, user_dict['phone'])

    def test_update_user(self):
        phone = "123456"
        password = "123456"
        nickname = "nick"
        avatar = "avatar"
        user = User(phone, password, nickname, avatar)
        User.insert_user(user)
        user_dict = loads(User.get_user(user._id))
        u_phone = "1234567"
        user_dict['phone'] = u_phone
        self.assertEquals("", User.update_user(user_dict))
        user_dict = loads(user.get_user(user._id))
        self.assertEquals(u_phone, user_dict['phone'])

    def test_add_focus_story(self):
        # create user
        phone = "123456"
        password = "123456"
        nickname = "nick"
        avatar = "avatar"
        user = User(phone, password, nickname, avatar)
        User.insert_user(user)
        # create story
        title = "test title"
        story = Story(title)
        Story.insert_story(story)
        self.assertEquals("", User.add_focus_story(user._id, story._id))
        user.focus_stories.append(story._id)
        self.assertEquals(user.__dict__, loads(User.get_user(user._id)))

    def test_add_focus_user(self):
        phone = "123456"
        password = "123456"
        nickname = "nick"
        avatar = "avatar"
        user = User(phone, password, nickname, avatar)
        focused_user = User(phone, password, nickname, avatar)
        User.insert_user(user)
        User.insert_user(focused_user)
        User.add_focus_user(user._id, focused_user._id)
        user.focus_users.append(focused_user._id)
        self.assertEquals(user.__dict__, loads(User.get_user(user._id)))

class StoryTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        collection = db['story']
        collection.remove({})

    def test_get_as_json(self):
        title = "test title"
        story = Story(title)
        story_dict = story.get_as_json()
        self.assertEquals(title, story_dict['title'])

    def test_insert_story(self):
        title = "test title"
        story = Story(title)
        self.assertEquals("", Story.insert_story(story))

    def test_get_story_by_id(self):
        title = "test title"
        story = Story(title)
        Story.insert_story(story)
        self.assertEquals(story.__dict__, loads(Story.get_story_by_id(story._id)))

    def test_get_story_by_current_owner(self):
        current_owner = 1
        title = "test title"
        story = Story(title)
        story.current_owner = current_owner
        Story.insert_story(story)
        self.assertEquals(story._id, loads(Story.get_story_by_current_owner(current_owner))[0]['_id'])

    def test_get_story_by_fields(self):
        pass

    def test_update_story(self):
        title = "test title"
        story = Story(title)
        Story.insert_story(story)
        story_dict = loads(Story.get_story_by_id(story._id))
        u_title = "updated title"
        story_dict['title'] = u_title
        self.assertEquals("", Story.update_story(story_dict))
        story_dict = loads(Story.get_story_by_id(story._id))
        self.assertEquals(u_title, story_dict['title'])

class ParagraphTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        collection = db['paragraph']
        collection.remove({})

    def test_get_as_json(self):
        author_id = 1
        story_id = 1
        paragraph = Paragraph(author_id, story_id)
        para_dict = paragraph.get_as_json()
        self.assertEquals(author_id, para_dict['author_id'])
        self.assertEquals(story_id, para_dict['story_id'])

    def test_insert_paragraph(self):
        author_id = 1
        story_id = 1
        paragraph = Paragraph(author_id, story_id)
        self.assertEquals("", Paragraph.insert_paragraph(paragraph))

    def test_get_one_paragraph(self):
        author_id = 1
        story_id = 1
        paragraph = Paragraph(author_id, story_id)
        Paragraph.insert_paragraph(paragraph)
        self.assertEquals(paragraph.__dict__, loads(Paragraph.get_paragraph(paragraph._id)))

    def test_get_all_paragraph(self):
        para_num = 3
        para_id_set = set()
        for i in range(para_num):
            author_id = i
            story_id = i
            paragraph = Paragraph(author_id, story_id)
            para_id_set.add(paragraph._id)
            Paragraph.insert_paragraph(paragraph)
        actual_para_list = loads(Paragraph.get_paragraph())
        actual_para_id_set = set()
        for actual_para in actual_para_list:
            actual_para_id_set.add(actual_para['_id'])
        self.assertEquals(actual_para_id_set, para_id_set)

    def test_get_paragraph_by_story_id(self):
        author_id = 1
        story_id = 1
        paragraph = Paragraph(author_id, story_id)
        Paragraph.insert_paragraph(paragraph)
        self.assertEquals(paragraph._id, loads(Paragraph.get_paragraph_by_story_id(story_id))[0]['_id'])

    def test_get_paragraph_by_fields(self):
        pass

    def test_update_paragraph(self):
        author_id = 1
        story_id = 1
        paragraph = Paragraph(author_id, story_id)
        Paragraph.insert_paragraph(paragraph)
        para_dict = loads(Paragraph.get_paragraph(paragraph._id))
        u_content = "test content"
        para_dict['content'] = u_content
        self.assertEquals("", Paragraph.update_paragraph(para_dict))
        para_dict = loads(Paragraph.get_paragraph(paragraph._id))
        self.assertEquals(u_content, para_dict['content'])

    def test_toggle_user_favours(self):
        # create paragraph
        author_id = 1
        story_id = 1
        paragraph = Paragraph(author_id, story_id)
        Paragraph.insert_paragraph(paragraph)
        # create user
        phone = "123456"
        password = "123456"
        nickname = "nick"
        avatar = "avatar"
        user = User(phone, password, nickname, avatar)
        User.insert_user(user)
        # favour
        Paragraph.toggle_user_favours(paragraph._id, user._id)
        paragraph.favour_users.append(user._id)
        self.assertEquals(paragraph.__dict__, loads(Paragraph.get_paragraph(paragraph._id)))
        Paragraph.toggle_user_favours(paragraph._id, user._id)
        paragraph.favour_users.remove(user._id)
        self.assertEquals(paragraph.__dict__, loads(Paragraph.get_paragraph(paragraph._id)))
"""

class UserBpTestCase(unittest.TestCase):

    def setUp(self):
        self.app = application.app.test_client()
        # insert user
        phone = "123456"
        password = "123456"
        avatar = "avatar"
        user = User(phone, password, avatar)
        User.insert_user(user)

    def tearDown(self):
        for name in ["message", "user", "story", "paragraph"]:
            db.drop_collection(name)

    def login(self, phone=None, password=None):
        headers = [("Content-Type", "application/json")]
        data = dict()
        if phone != None:
            data["phone"] = phone
        if password != None:
            data["password"] = password
        json_data = dumps(data)
        json_data_length = len(json_data)
        headers.append(("Content-Length", json_data_length))
        return self.app.post("/user/login", headers=headers, data=json_data)

    def test_login(self):
        rv = self.login("123456", "123456")
        self.assertEquals(200, loads(rv.data)["status"])

    # def test_login_empty_phone(self):
    #     rv = self.login()
    #     print rv

if __name__ == '__main__':
    unittest.main()
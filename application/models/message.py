from bson.objectid import ObjectId
from bson.json_util import dumps
from datetime import datetime
from pymongo.errors import *

from ..utils.db import db

class Message:
    # {
    #     id: 'xxx',
    #     sender: system_user_id,
    #     create_time: 'xxx',
    #     content: 'xxx'
    # }
    def __init__(self, sender, content, id=None, create_time = None):
        # if id is None:
        self._id = ObjectId()
        # else:
        #     self._id = ObjectId(id)
        # if create_time is None:
        self.create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # else:
        #     self.create_time = create_time
        self.sender = sender
        self.content = content

    
    #return the class as json
    def get_as_json(self):
        return self.__dict__

    # #convert json to message object
    # @staticmethod
    # def build_from_json(json_data):
    #     if json_data is not None:
    #         try:
    #             return Message(json_data.get('_id', None),
    #                 json_data['sender'],
    #                 json_data['content'],
    #                 json_data.get('create_time', None)
    #                 )
    #         except KeyError as e:
    #             raise Exception("Key not found in json_data: {}".format(e.message))
    #     else:
    #         raise Exception("No data to create message from!")

    #insert message
    @staticmethod
    def insert_message(i_message):
        collection =  db['message']
        if i_message is not None:
            try:
                collection.insert_one(i_message.get_as_json())
                return ""
            except DuplicateKeyError as e:
                return "Insert fail due to duplicate key."
            except PyMongoError as e:
                return "Insert fail due to unkown reason."
        else:
            return "Insert fail due to unvalid parameter."

    #get messages by id or get all messages 
    #json type: list or dict
    @staticmethod
    def get_message(id = None):
        collection =  db['message']
        if id is None:
            return dumps(collection.find({}))
        else:
            return dumps(collection.find_one({"_id":id}))

    #get a lists of message by sender
    #json type: list
    @staticmethod
    def get_message_by_sender(sender):
        collection =  db['message']
        return dumps(collection.find({"sender":sender}))

    #params can be json or dict
    #update message
    @staticmethod
    def update_message(u_message):
        collection =  db['message']
        if u_message is not None:
            try:
                # m_json = u_message.get_as_json()
                result = collection.replace_one({'_id':u_message['_id']}, u_message)
                if result.modified_count == 0:
                    return "Update fail due to not existing id."
                else:
                    return ""
            except PyMongoError as e:
                return "Update fail due to unkown reason."
        else:
            return "Update fail due to unvalid parameter."

    #delete message
    @staticmethod
    def delete_message(id):
        collection = db['message']
        try:
            result = collection.delete_one({'_id':id})
            if result.deleted_count == 0:
                return "Delete fail due to not existing id."
            else:
                return ""
        except PyMongoError as e:
            return "Update fail due to unkown reason."

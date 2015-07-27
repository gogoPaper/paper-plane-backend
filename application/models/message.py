from bson.objectid import ObjectId
from bson.json_util import dumps
from datetime import datetime

from ..utils.db import db

class Message:
    # {
    #     id: 'xxx',
    #     sender: system_user_id,
    #     create_time: 'xxx',
    #     content: 'xxx'
    # }
    def __init__(self, sender, content, id=None, create_time = None):
        if id is None:
            self._id = ObjectId()
        else:
            self._id = ObjectId(id)
        if create_time is None:
            self.create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.create_time = create_time

        self.sender = sender
        self.content = content

    
    #return the class as json
    def get_as_json(self):
        return self.__dict__

    #convert json to message object
    @staticmethod
    def build_from_json(json_data):
        if json_data is not None:
            try:
                return Message(json_data.get('id', None),
                    json_data['sender'],
                    json_data['content'],
                    json_data.get('create_time', None)
                    )
            except KeyError as e:
                raise Exception("Key not found in json_data: {}".format(e.message))
        else:
            raise Exception("No data to create message from!")

    #return _id(string)
    @staticmethod
    def add_message(c_message):
        collection =  db['message']
        if c_message is not None:
            create_id = collection.insert(c_message.get_as_json())
            return str(create_id)
        else:
            raise Exception("Nothing to save, because parameter is None")

    #return json
    @staticmethod
    def read_message(id = None):
        collection =  db['message']
        if id is None:
            return dumps(collection.find({}))
        else:
            return dumps(collection.find({"_id":ObjectId(id)}))

    #return json
    @staticmethod
    def read_by_sender(sender):
        collection =  db['message']
        return dumps(collection.find({"sender":sender}))

    #return _id(string)
    @staticmethod
    def update_message(u_message):
        collection =  db['message']
        if u_message is not None:
            update_id = collection.save(u_message.get_as_json())
            return str(update_id)
        else:
            raise Exception("Nothing to update, because parameter is None")

    #return _id(string)
    @staticmethod
    def delete_message(r_message):
        collection = db['message']
        if r_message is not None:
            remove_id = collection.remove(r_message.get_as_json())
            return str(remove_id)
        else:
            raise Exception("Nothing to delete, because parameter is None")

from ..utils.db import collection

class User:
    # {
    #     id: 'xxx',
    #     token: 'xxx',
    #     phone: 'xxx',
    #     password: 'xxx',
    #     nickname: 'xxx',
    #     avatar: 'url',
    #     focus_storis: [story_ids],
    #     focus_users?: [user_ids],
    #     degree: <number>,
    #     experience_value: <number>
    # }
    def __init__(self, arg):
        self.arg = arg

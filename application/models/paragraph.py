from ..utils.db import collection

class Paragraph:
    # {
    #     id: 'xxx',
    #     author_id: 'xx',
    #     story_id: 'xx'
    #     create_time: 'xxx',
    #     favours: Number,
    #     content: 'xxx',
    #     pictures: ['urlxxx', ...]
    # }

    def __init__(self, arg):
        self.arg = arg

    

    # def __init__(self):
    #     pass

    # def test(self):
    #     return collection.find_one()
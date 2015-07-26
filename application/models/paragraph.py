from . import db

class paragraph:
    def __init__(self):
        self.collection = db['test']
    
    def test(self):
        return self.collection.find_one()
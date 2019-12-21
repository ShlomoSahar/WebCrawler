class HashMap(dict):

    def __init__(self):
        self = dict()

    def put(self, key, value):
        self[key] = value

    def contains_key(self, key):
        return key in self

    def get(self, key):
        return self[key]

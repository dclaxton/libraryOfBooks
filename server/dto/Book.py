
class Book:
    def __init__(self, id, name, author, hasRead, available):
        self.id = id
        self.name = name
        self.author = author
        self.hasRead = hasRead
        self.available = available

    #for serializing python objects with json.dumps
    def encode(self):
        return self.__dict__
class User(object):

    def __init__(self, name):
        self.name = name

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.name

    @staticmethod
    def get(id):
        return User(id)
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, email, password=None, created_at=None):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.created_at = created_at
        self.is_admin = True 
        self.is_active = True

    def get_id(self):
        return str(self.id)
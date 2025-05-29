from database import Database
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, email, password=None, phone=None, created_at=None, is_active=None):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.phone = phone
        self.created_at = created_at
        self.is_active = is_active

    def get_id(self):
        return f"u_{self.id}"
        
    @property
    def is_admin(self):
        return False
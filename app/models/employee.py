from flask_login import UserMixin

class Employee(UserMixin):
    def __init__(self, id, username, cpf, created_at=None, hired_at=None, password=None, is_active=True, email=None):
        self.id = id
        self.username = username
        self.cpf = cpf
        self.created_at = created_at
        self.hired_at = hired_at
        self.password = password
        self._is_active = is_active
        self.email = email
        
    def get_id(self):
        return f"e_{self.id}"
        
    @property
    def is_active(self):
        return self._is_active
        
    @property
    def is_admin(self):
        return True
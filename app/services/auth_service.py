import hashlib
from app.repositories.user_repository import IUserRepository
from app.models.user import User

class AuthService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def register_user(self, username, password, email):
        if self.user_repository.fetch_user_by_email(email):
            raise ValueError("email ja cadastrado")

        hashed_psswrd = self._hash_password(password)
        user = self.user_repository.insert_user(username, hashed_psswrd, email)
        if not user:
            raise ValueError("falha ao cadastrar usuario")

    def login_user(self, email, password):
        user = self.user_repository.fetch_user_by_email(email)
        print(user)
        if not user or not self._verify_password(password, user.password): 
            return None
        return user

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def _verify_password(self, password, hashed_psswrd):
        return self._hash_password(password) == hashed_psswrd

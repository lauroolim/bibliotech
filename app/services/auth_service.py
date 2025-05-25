import hashlib
from app.repositories.user_repository import IUserRepository
from app.repositories.employee_repository import IEmployeeRepository
from app.models.user import User
from app.models.employee import Employee

class AuthService:
    def __init__(self, user_repository: IUserRepository, employee_repository: IEmployeeRepository):
        self.user_repository = user_repository
        self.employee_repository = employee_repository

    def register_user(self, username, password, email):
        if self.user_repository.fetch_user_by_email(email):
            raise ValueError("email já cadastrado")

        hashed_password = self._hash_password(password)
        user = self.user_repository.insert_user(username, hashed_password, email)
        if not user:
            raise ValueError("falha ao cadastrar usuario")

    def login_user(self, email, password):
        user = self.user_repository.fetch_user_by_email(email)
        if not user or not self._verify_password(password, user.password): 
            return None
        return user

    def login_employee(self, cpf, password):
        employee = self.employee_repository.fetch_employee_by_cpf(cpf)
        if not employee or not self._verify_password(password, employee.password):
            return None
        return employee

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def _verify_password(self, password, hashed_password):
        return self._hash_password(password) == hashed_password
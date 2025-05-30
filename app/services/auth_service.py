from app.utils.hash_password import hash_password
from app.repositories.user_repository import IUserRepository
from app.repositories.employee_repository import IEmployeeRepository
from app.models.user import User
from app.models.employee import Employee
from app.utils.hash_password import verify_password

class AuthService:
    def __init__(self, user_repository: IUserRepository, employee_repository: IEmployeeRepository):
        self.user_repository = user_repository
        self.employee_repository = employee_repository

    def login_user(self, email, password):
        user = self.user_repository.fetch_user_by_email(email)
        if not user or not verify_password(password, user.password): 
            return None
        return user

    def login_employee(self, cpf, password):
        employee = self.employee_repository.fetch_employee_by_cpf(cpf)
        if not employee or not verify_password(password, hashed_new_password=employee.password):
            return None
        return employee
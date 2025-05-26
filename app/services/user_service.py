from app.repositories.user_repository import IUserRepository
from app.models.user import User
from app.models.employee import Employee
from app.utils.hash_password import hash_password

class UserService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def register_user(self, username, password, email, phone):
        if self.user_repository.fetch_user_by_email(email):
            raise ValueError("email já cadastrado")

        hashed_password = hash_password(password)
        user = self.user_repository.insert_user(username, hashed_password, email, phone)
        if not user:
            raise ValueError("falha no service de cadastro de usuario")

    def list_users(self, page=1, per_page=10, search=None):
        users = self.user_repository.fetch_all_users(page, per_page, search)
        total_count = self.user_repository.count_users(search)  
        total_pages = (total_count + per_page - 1) // per_page
        
        return {
            'users': users,
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages,
            'total_count': total_count,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }
    
    def delete_user(self, user_id):
        user = self.user_repository.fetch_user_by_id(user_id)
        if not user:
            raise ValueError("usuario não encontrado")
        
        self.user_repository.delete_user(user_id)
        return True

    def update_user(self, user_id, username, email):
        user = self.user_repository.fetch_user_by_id(user_id)
        if not user:
            raise ValueError("usuario não encontrado")
        
        self.user_repository.update_user(user_id, username, email)
        return True

from app.repositories.user_repository import IUserRepository
from app.models.user import User
from app.models.employee import Employee
from app.utils.hash_password import hash_password
from app.utils.hash_password import verify_password
import logging
logger = logging.getLogger(__name__)
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
        
        for user in users:
            logger.info(f"DEBUG: User {user.id} - {user.username} - is_active: {user.is_active}")

        return {
            'users': users,
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages,
            'total_count': total_count,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }


    def deactivate_user(self, user_id):
        if not user_id:
            raise ValueError("ID do usuário é obrigatório")
        user_before = self.user_repository.fetch_user_by_id(user_id)
        logger.info(f"DEBUG ANTES: User {user_id} - is_active: {user_before.is_active if user_before else 'NOT_FOUND'}")
        
        result = self.user_repository.soft_delete_user(user_id)
        logger.info(f"DEBUG RESULTADO: soft_delete_user retornou: {result}")
        
        user_after = self.user_repository.fetch_user_by_id(user_id)
        logger.info(f"DEBUG DEPOIS: User {user_id} - is_active: {user_after.is_active if user_after else 'NOT_FOUND'}")
        
        if not result:
            raise ValueError("Erro ao desativar usuário")
        return result

    def activate_user(self, user_id):
        if not user_id:
            raise ValueError("ID do usuário é obrigatório")
        
        user = self.user_repository.fetch_user_by_id(user_id)
        if not user:
            raise ValueError("Usuário não encontrado")
        
        if user.is_active:
            raise ValueError("Usuário já está ativo")
        
        result = self.user_repository.activate_user(user_id)
        
        if not result:
            raise ValueError("Erro ao reativar usuário")
        
        return result

    def update_user(self, user_id, username, email, phone=None, password=None):
        if not user_id:
            raise ValueError("userID  obrigatorio")
        
        result = self.user_repository.update_user(
            user_id, 
            username=username,
            email=email,
            phone=phone
        )
        if not result:
            raise ValueError("Erro ao atualizar dados do user")
        
        if password:
            password_hash = hash_password(password)
            password_result = self.user_repository.update_password(user_id, password_hash)  # ✅ Método correto
            
            if not password_result:
                raise ValueError("Erro ao atualizar senha do user")
        return True 

    def get_user_active_loans(self, user_id):
        user = self.user_repository.fetch_user_by_id(user_id)
        if not user:
            raise ValueError("user não encontrado")
        
        return self.user_repository.fetch_user_active_loans(user_id, 5)

    def get_user_profile_data(self, user_id: int):
        try:
            user = self.user_repository.fetch_user_by_id(user_id)
            if not user:
                raise ValueError("Usuário não encontrado")
            
            stats = self.user_repository.fetch_user_loan_stats(user_id)
            logger.info(f"Stats retornadas do repository: {stats}")
            
            return {
                'user': user,
                'active_loans': stats.get('active', 0),
                'overdue_loans': stats.get('overdue', 0),  
                'total_loans': stats.get('total', 0)
            }
        except Exception as e:
            logger.error(f"Erro no user_service.get_user_profile_data: {str(e)}")
            raise


    def change_password(self, user_id, current_password, new_password):
        user = self.user_repository.fetch_user_by_id(user_id)
        if not user:
            raise ValueError("user não encontrado")
        
        if not verify_password(current_password, user.password):
            raise ValueError("senha atual incorreta")
        
        hashed_new_password = hash_password(new_password)
        self.user_repository.update_user_password(user_id, hashed_new_password)
        return True
    
    def get_user_by_id(self, user_id):
        user = self.user_repository.fetch_user_by_id(user_id)
        if not user:
            raise ValueError("user não encontrado")
        
        return user
    
    def search_user_by_email(self, email):
        if not email or not email.strip():
            raise ValueError("email obrigatório")
        
        email = email.strip().lower()
        
        user = self.user_repository.fetch_user_by_email(email)

        return user
    
    def search_user_by_username(self, username):
        if not username or not username.strip():
            raise ValueError("username obrigatorio")
        
        return self.user_repository.fetch_user_by_username(username.strip())

    def search_user(self, search_term):
        if not search_term or not search_term.strip():
            raise ValueError("termo de busca obrigatorio")
        
        search_term = search_term.strip()
        
        if '@' in search_term:
            return self.search_user_by_email(search_term)
        else:
            return self.search_user_by_username(search_term)
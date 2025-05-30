from abc import ABC, abstractmethod
from app.models.user import User
import logging

logger = logging.getLogger(__name__)

class IUserRepository(ABC):
    @abstractmethod
    def insert_user(self, username: str, password: str, email: str, phone: str) -> bool:
        pass

    @abstractmethod
    def fetch_user_by_email(self, email: str) -> User:
        pass
    
    @abstractmethod
    def fetch_user_by_id(self, user_id: int) -> User:
        pass

    @abstractmethod
    def update_user(self, user_id: int, username: str, email: str, phone: str) -> bool:
        pass

    @abstractmethod
    def soft_delete_user(self, user_id: int) -> bool:
        pass

    @abstractmethod
    def fetch_all_users(self, page: int, per_page: int) -> list[User]:
        pass

    @abstractmethod
    def fetch_user_loan_stats(self, user_id: int) -> dict:
        pass

    @abstractmethod
    def fetch_user_active_loans(self, user_id: int, limit: int = 5) -> list:
        pass
    @abstractmethod
    def update_user_password(self, user_id: int, hashed_new_password: str) -> bool:
        pass
class PSQLUserRepository(IUserRepository):
    def __init__(self, db):
        self.db = db

    def insert_user(self, username, password, email, phone):
        query = "INSERT INTO users (username, password, email, phone) VALUES (?, ?, ?, ?)"
        params = [username, password, email, phone]  

        try:
            self.db.execute_query(query, params)
            return True
        except Exception as e:
            logger.error(f"Erro ao inserir usuário: {str(e)}")
            return False

    def fetch_user_by_email(self, email):
        query = "SELECT id, username, email, phone, password, created_at, is_active FROM users WHERE email = ?"
        params = [email]

        try:
            cursor = self.db.execute_query(query, params)
            user = cursor.fetchone()

            if user:
                return User(
                    id=user[0], 
                    username=user[1], 
                    email=user[2], 
                    phone=user[3],
                    password=user[4], 
                    created_at=user[5],
                    is_active=user[6] 
                )
            return None
        except Exception as e:
            logger.error(f"falha ao buscar usuario no banco: {str(e)}")
            return None

    def fetch_user_by_id(self, user_id):
        query = "SELECT id, username, email, phone, password, created_at, is_active FROM users WHERE id = ?"
        params = [int(user_id)]  

        try:
            cursor = self.db.execute_query(query, params)
            user = cursor.fetchone()

            if user:
                return User(
                    id=user[0], 
                    username=user[1], 
                    email=user[2],
                    phone=user[3],
                    password=user[4], 
                    created_at=user[5],
                    is_active=user[6]
                )
            return None
        except Exception as e:
            logger.error(f"falha ao buscar usuario no banco: {str(e)}")
            return None
    
    def update_user(self, user_id, username, email, phone):
        query = "UPDATE users SET username = ?, email = ?, phone = ? WHERE id = ?"
        params = [username, email, phone, int(user_id)]  

        try:
            self.db.execute_query(query, params)
            return True
        except Exception as e:
            logger.error(f"falha ao atualizar usuario no banco: {str(e)}")
            return False

    def update_password(self, user_id, hashed_new_password):
        query = "UPDATE users SET password = ? WHERE id = ?"
        params = [hashed_new_password, int(user_id)]  

        try:
            cursor = self.db.execute_query(query, params)
            affected_rows = cursor.rowcount
            return affected_rows > 0
        except Exception as e:
            logger.error(f"repository falha ao atualizar senha do usuario no banco: {str(e)}")
            return False

    def soft_delete_user(self, user_id: int):
        query = "UPDATE users SET is_active = FALSE, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
        params = [user_id]
        
        try:
            cursor = self.db.execute_query(query, params)
            affected_rows = cursor.rowcount
            cursor.close()

            logger.info(f"user {user_id} desativado no banco")
            
            return affected_rows > 0
        except Exception as e:
            logger.error(f"repository falhou ao desativar user {user_id}: {str(e)}")
            return False

    def fetch_all_users(self, page, per_page, search: str = None):

        offset = (page - 1) * per_page
        
        if search:
            query = """
                SELECT id, username, email, phone, password, created_at, is_active 
                FROM users 
                WHERE username LIKE ? OR email LIKE ? 
                ORDER BY id 
                LIMIT ? OFFSET ?
            """
            search_param = f"%{search}%"
            params = [search_param, search_param, per_page, offset]
        else:
            query = "SELECT id, username, email, phone, password, created_at, is_active FROM users ORDER BY id LIMIT ? OFFSET ?"
            params = [per_page, offset]

        try:
            cursor = self.db.execute_query(query, params)
            users = cursor.fetchall()
            cursor.close()
            if users:
                return [
                    User(
                        id=user[0], 
                        username=user[1], 
                        email=user[2],
                        phone=user[3], 
                        password=user[4], 
                        created_at=user[5],
                        is_active=user[6]
                    ) for user in users
                ]
            return []
        except Exception as e:
            logger.error(f"falha ao buscar todos os usuarios no banco: {str(e)}")
            return []

    def count_users(self, search: str = None):

        if search:
            query = "SELECT COUNT(*) FROM users WHERE username LIKE ? OR email LIKE ?"
            search_param = f"%{search}%"
            params = [search_param, search_param]
        else:
            query = "SELECT COUNT(*) FROM users"
            params = []
        
        try:
            cursor = self.db.execute_query(query, params)
            result = cursor.fetchone()
            return result[0] if result else 0
        except Exception as e:
            logger.error(f"falha ao contar total de usuários: {str(e)}")
            return 0
    
    def fetch_user_loan_stats(self, user_id: int):
        queries = {
            'active': "SELECT COUNT(*) FROM loans WHERE user_id = ? AND returned_at IS NULL AND expected_return_date >= CURRENT_DATE",
            'overdue': "SELECT COUNT(*) FROM loans WHERE user_id = ? AND returned_at IS NULL AND expected_return_date < CURRENT_DATE",
            'total': "SELECT COUNT(*) FROM loans WHERE user_id = ?"
        }
        
        stats = {}
        try:
            for key, query in queries.items():
                cursor = self.db.execute_query(query, [user_id])
                result = cursor.fetchone()
                stats[key] = result[0] if result else 0
                cursor.close()
            
            return stats
        except Exception as e:
            logger.error(f"falha no repository ao buscar estatísticas do user {user_id}: {str(e)}")
            return {'active': 0, 'overdue': 0, 'total': 0}

    def fetch_user_active_loans(self, user_id: int, limit: int = 5):

        query = """
            SELECT l.id, l.expected_return_date, l.created_at, b.title 
            FROM loans l
            JOIN books b ON l.book_id = b.id
            WHERE l.user_id = ? AND l.returned_at IS NULL
            ORDER BY l.expected_return_date DESC
            LIMIT ?
        """
        params = [user_id, limit]

        try:
            cursor = self.db.execute_query(query, params)
            loans = cursor.fetchall()
            cursor.close()

            return [
                {
                    'id': loan[0],
                    'expected_return_date': loan[1],
                    'created_at': loan[2],
                    'book_title': loan[3]
                } for loan in loans
            ]
        except Exception as e:
            logger.error(f"falha no repository ao buscar emprestimos ativos do user {user_id}: {str(e)}")
            return []
    
    def update_user_password(self, user_id: int, hashed_new_password: str) -> bool:
        query = "UPDATE users SET password = ? WHERE id = ?"
        params = [hashed_new_password, user_id]

        try:
            cursor = self.db.execute_query(query, params)
            affected_rows = cursor.rowcount
            cursor.close()
            return affected_rows > 0
        except Exception as e:
            logger.error(f"falha ao inser nova senha do user {user_id} no banco: {str(e)}")
            return False
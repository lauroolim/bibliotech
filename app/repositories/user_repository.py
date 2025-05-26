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
    def delete_user(self, user_id: int) -> bool:
        pass

    @abstractmethod
    def fetch_all_users(self, page: int, per_page: int) -> list[User]:
        pass

class PSQLUserRepository(IUserRepository):
    def __init__(self, db):
        self.db = db

    def insert_user(self, username, password, email, phone):
        query = "INSERT INTO users (username, password, email, phone) VALUES (?, ?, ?, ?)"
        params = [username, password, email, phone]  # Corrigido para incluir phone

        try:
            self.db.execute_query(query, params)
            return True
        except Exception as e:
            logger.error(f"Erro ao inserir usuário: {str(e)}")
            return False

    def fetch_user_by_email(self, email):
        query = "SELECT id, username, email, phone, password, created_at FROM users WHERE email = ?"
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
                    created_at=user[5]
                )
            return None
        except Exception as e:
            logger.error(f"falha ao buscar usuario no banco: {str(e)}")
            return None

    def fetch_user_by_id(self, user_id):
        query = "SELECT id, username, email, phone, password, created_at FROM users WHERE id = ?"
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
                    created_at=user[5]
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

    def delete_user(self, user_id):
        query = "DELETE FROM users WHERE id = ?"
        params = [int(user_id)]  

        try:
            self.db.execute_query(query, params)
            return True
        except Exception as e:
            logger.error(f"falha ao deletar usuario no banco: {str(e)}")
            return False

    def fetch_all_users(self, page, per_page):
        offset = (page - 1) * per_page
        query = "SELECT id, username, email, phone, password, created_at FROM users ORDER BY id LIMIT ? OFFSET ?"
        params = [per_page, offset]

        try:
            cursor = self.db.execute_query(query, params)
            users = cursor.fetchall()

            if users:
                return [
                    User(
                        id=user[0], 
                        username=user[1], 
                        email=user[2],
                        phone=user[3], 
                        password=user[4], 
                        created_at=user[5]
                    ) for user in users
                ]
            return []
        except Exception as e:
            logger.error(f"falha ao buscar todos os usuarios no banco: {str(e)}")
            return []

    def count_users(self):
        query = "SELECT COUNT(*) FROM users"
        
        try:
            cursor = self.db.execute_query(query)
            result = cursor.fetchone()
            return result[0] if result else 0
        except Exception as e:
            logger.error(f"falha ao contar total de usuários: {str(e)}")
            return 0
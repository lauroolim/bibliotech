from abc import ABC, abstractmethod
from app.models.user import User
import logging

logger = logging.getLogger(__name__)

class IEmployeeRepository(ABC):
    @abstractmethod
    def insert_user(self, username: str, password: str, email: str) -> bool:
        pass

    @abstractmethod
    def fetch_user_by_email(self, email: str) -> User:
        pass
    
    @abstractmethod
    def fetch_user_by_id(self, user_id: int) -> User:
        pass

class PSQLUserRepository(IUserRepository):
    def __init__(self, db):
        self.db = db

    def insert_user(self, username, password, email):
        query = "INSERT INTO users (username, password, email) VALUES (?, ?, ?)"
        params = [username, password, email]  

        try:
            self.db.execute_query(query, params)
            return True
        except Exception as e:
            print(f"Erro ao inserir usuário: {str(e)}")
            return False

    def fetch_user_by_email(self, email):
        query = "SELECT id, username, email, password, created_at FROM users WHERE email = ?"
        params = [email]

        try:
            cursor = self.db.execute_query(query, params)
            user = cursor.fetchone()

            if user:
                return User(id=user[0], username=user[1], email=user[2], password=user[3], created_at=user[4])
            return None
        except Exception as e:
            logger.error(f"falha ao buscar usuario no banco: {str(e)}")
            return None

    def fetch_user_by_id(self, user_id):
        query = "SELECT id, username, email, password, created_at FROM users WHERE id = ?"
        params = [int(user_id)]  

        try:
            cursor = self.db.execute_query(query, params)
            user = cursor.fetchone()

            if user:
                return User(id=user[0], username=user[1], email=user[2], password=user[3], created_at=user[4])
            return None
        except Exception as e:
            logger.error(f"falha ao buscar usuario no banco: {str(e)}")
            return None
from database import Database

class User:
    @classmethod
    def insert_user(cls, username, password):
        query = "INSERT INTO users (username, password) VALUES (?, ?)"
        params = (username, password)
        try:
            Database.execute_query(query, params)
            return True
        except Exception as e:
            print(f"erro ao inserir usuario no banco: {str(e)}")
            return False

    @classmethod
    def fetch_user(cls, email):
        query = "SELECT * FROM users WHERE email = ?"
        params = (email)
        try:
            cursor = Database.execute_query(query, params)
            user = cursor.fetchone()
            return user
        except Exception as e:
            print(f"erro ao recuperar usuario do banco: {str(e)}")
            return None
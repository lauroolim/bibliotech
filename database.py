import pyodbc
import os

class Database:  
    _instance = None

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)
            
    @classmethod
    def get_connection(cls):
        return pyodbc.connect(os.getenv('DB_ODBC_STRING'))

    @classmethod
    def execute_query(cls, query, params=None, commit=True):
        conn = cls.get_connection()
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            if commit:
                conn.commit()
                
            return cursor
        except Exception as e:
            if commit:
                conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def init_app(cls, app):
        try:
            conn = cls.get_connection()
            conn.close()
            print("Conexão com o banco de dados estabelecida com sucesso")
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {str(e)}")
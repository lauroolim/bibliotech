import pyodbc
import os
from flask import current_app

class Database:  
    _instance = None

    @classmethod
    def init_app(cls, app): 
        app.db = cls
        with app.app_context():
            cls.test_conn()

    @classmethod
    def get_connection(cls):
        return pyodbc.connect(current_app.config['DB_ODBC_STRING'])

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
    def test_conn(cls):
        try:
            conn = cls.get_connection()
            conn.close()
            print("Conexão com o banco de dados estabelecida com sucesso")
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {str(e)}")
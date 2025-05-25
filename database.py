import pyodbc
import os
from flask import current_app
import logging

logger = logging.getLogger(__name__)

class Database:  
    _instance = None

    @classmethod
    def init_app(cls, app): 
        app.db = cls
        with app.app_context():
            cls.test_conn()

    @classmethod
    def get_connection(cls):
        conn = pyodbc.connect(current_app.config['DB_ODBC_STRING'])
        cursor = conn.cursor()
        cursor.execute("SET search_path TO bibliotech, public")
        cursor.close()
        return conn
 
    @classmethod
    def execute_query(cls, query, params=None, commit=True):
        conn = cls.get_connection()
        conn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
        conn.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
        conn.setencoding(encoding='utf-8')
        
        is_select = query.strip().upper().startswith("SELECT")

        cursor = conn.cursor()
        try:
            logger.debug(f"executando query: {query} e params: {params}")
            
            if params:
                if is_select:
                    cursor.execute(query, *params)
                else:
                    cursor.execute(query, params)
            else:
                cursor.execute(query)

            if is_select:
                return cursor
            else:
                if commit:
                    conn.commit()
                return cursor
        except Exception as e:
            logger.error(f"erro ao executar query: {e}")
            logger.error(f"query: {query}")
            logger.error(f"params: {params}")
            if commit:
                conn.rollback()
            raise
        finally:
            if not is_select:
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
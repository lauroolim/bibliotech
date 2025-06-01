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
        cursor.execute("SET search_path TO bibliotech")
        cursor.close()
        return conn
 
    @classmethod
    def execute_query(cls, query, params=None, commit=True):
        conn = cls.get_connection()
        conn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
        conn.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
        conn.setencoding(encoding='utf-8')
        
        is_select = query.strip().upper().startswith("SELECT")
        is_returning = "RETURNING" in query.upper()

        cursor = conn.cursor()
        try:
            logger.debug(f"executando query: {query} e params: {params}")
            
            if params:
                if is_select or is_returning:
                    cursor.execute(query, *params)
                else:
                    cursor.execute(query, params)
            else:
                cursor.execute(query)

            if is_returning and commit:
                conn.commit()
                logger.debug("Commit realizado para query RETURNING")

            if is_select or is_returning:
                return cursor 
            else:
                if commit:
                    conn.commit()
                    logger.debug("Commit realizado")
                return cursor
        except Exception as e:
            logger.error(f"erro ao executar query: {e}")
            if commit:
                conn.rollback()
                logger.debug("Rollback realizado")

            cursor.close()
            conn.close()
            raise
        finally:
            if not (is_select or is_returning):
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
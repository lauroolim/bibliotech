import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_key')
    DEBUG = False
    
class DevelopmentConfig(Config):
    DEBUG = True
    #se der erro de conn tire o getenv e modifique a string direto
    DB_ODBC_STRING= os.getenv('DB_ODBC_STRING', 'DRIVER={PostgreSQL};SERVER=db;PORT=5432;DATABASE=bibliotech;UID=admin;PWD=root;')
class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
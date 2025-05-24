import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_key')
    DEBUG = False
    
class DevelopmentConfig(Config):
    DEBUG = True
    DB_ODBC_STRING= os.getenv('DB_ODBC_STRING', 'DRIVER={PostgreSQL};SERVER=localhost;DATABASE=bibliotech;UID=admin;PWD=root;PORT=5432;')
class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


from flask import Flask
from config import Config
from database import Database

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db = Database(app)
    
    @app.route('/test/')
    def test_page():
        return '<h1>testeeeee</h1>'

    return app
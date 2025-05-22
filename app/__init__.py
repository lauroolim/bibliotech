from flask import Flask
from config import config
from database import Database

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    from database import Database
    Database.init_app(app)

    @app.route('/test/')
    def test_page():
        return '<h1>testeeeee</h1>'

    return app
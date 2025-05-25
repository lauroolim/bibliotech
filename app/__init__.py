from flask import Flask, render_template
from config import config
from database import Database
from flask_login import LoginManager
from app.repositories.user_repository import PSQLUserRepository
from app.repositories.employee_repository import PSQLEmployeeRepository
from app.controllers.auth_controller import AuthController
import logging

login_manager = LoginManager()
login_manager.login_view = 'auth.login_user'  
login_manager.login_message = 'Por favor, faça login para acessar esta página.'
login_manager.login_message_category = 'info'

def create_app(config_name='development'):
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(config[config_name])

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(name)s: %(message)s'
    )

    app.logger.setLevel(logging.DEBUG)
  
    Database.init_app(app)
    login_manager.init_app(app)

    user_repository = PSQLUserRepository(Database)
    employee_repository = PSQLEmployeeRepository(Database)
    auth_controller = AuthController(user_repository, employee_repository)

    @login_manager.user_loader
    def load_user(user_id):
        if user_id.startswith('u_'):
            real_id = int(user_id[2:])
            return user_repository.fetch_user_by_id(real_id)
        elif user_id.startswith('e_'):
            real_id = int(user_id[2:])
            return employee_repository.fetch_employee_by_id(real_id)
        
        return None

    from app.routes.auth_routes import create_auth_blueprint
    app.register_blueprint(create_auth_blueprint(auth_controller))

    @app.route('/')
    def index():
        return render_template('index.html')

    return app
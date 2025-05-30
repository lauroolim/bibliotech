from flask import Flask, render_template
from config import config
from database import Database
from flask_login import LoginManager
import logging

from app.repositories.user_repository import PSQLUserRepository
from app.repositories.employee_repository import PSQLEmployeeRepository
from app.repositories.book_repository import PSQLBookRepository 
from app.repositories.loan_repository import PSQLLoanRepository

from app.services.loan_service import LoanService
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.services.book_service import BookService

from app.controllers.auth_controller import AuthController
from app.controllers.user_controller import UserController
from app.controllers.admin_controller import AdminController
from app.controllers.book_controller import BookController
from app.controllers.loan_controller import LoanController
from app.controllers.profile_controller import ProfileController

login_manager = LoginManager()
login_manager.login_view = 'auth.login_user'  
login_manager.login_message = 'faça login para acessar esta pagina'
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
    book_repository = PSQLBookRepository(Database)  
    loan_repository = PSQLLoanRepository(Database)

    loan_service = LoanService(loan_repository, user_repository, book_repository)
    user_service = UserService(user_repository)
    auth_service = AuthService(user_repository, employee_repository)

    book_controller = BookController(book_repository, loan_repository)
    auth_controller = AuthController(auth_service)
    user_controller = UserController(user_repository)
    admin_controller = AdminController(loan_service)  
    loan_controller = LoanController(loan_repository, user_repository, book_repository)
    profile_controller = ProfileController(user_service, loan_service)

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

    from app.routes.admin_routes import create_admin_blueprint
    app.register_blueprint(create_admin_blueprint(
        user_controller, 
        book_controller, 
        admin_controller,
        loan_controller
    ))
    
    from app.routes.book_routes import create_book_blueprint
    book_bp = create_book_blueprint(book_controller)
    app.register_blueprint(book_bp)

    from app.routes.profile_routes import create_profile_blueprint
    profile_bp = create_profile_blueprint(profile_controller)
    app.register_blueprint(profile_bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app
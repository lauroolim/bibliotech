from flask import Blueprint
from flask_login import login_required
from app.utils.decorators import admin_required

def create_admin_blueprint(user_controller, book_controller, admin_controller):
    admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

    @admin_bp.route('/dashboard', methods=['GET'])
    @login_required
    @admin_required
    def dashboard():
        return admin_controller.show_dashboard()

    @admin_bp.route('/register-user', methods=['GET', 'POST'])
    @login_required
    @admin_required
    def register_user():
        return user_controller.register_user()

    @admin_bp.route('/list-users', methods=['GET'])
    @login_required
    @admin_required
    def list_users():
        return user_controller.list_users()

    @admin_bp.route('/register-book', methods=['GET', 'POST'])
    @login_required
    @admin_required
    def register_book():
        return book_controller.register_book()
    
    @admin_bp.route('/register-author', methods=['GET', 'POST'])
    @login_required
    @admin_required
    def register_author():
        return book_controller.register_author()

    @admin_bp.route('/list-books', methods=['GET'])
    @login_required
    @admin_required
    def list_books():
        return book_controller.list_books()

    return admin_bp
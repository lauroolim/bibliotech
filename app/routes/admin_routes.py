from flask import Blueprint
from app.controllers.user_controller import UserController
from flask_login import login_required
from app.utils.decorators import admin_required
from app.controllers.admin_controller import AdminController

def create_admin_blueprint(user_controller):
    admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
    admin_controller = AdminController()

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
    def list_user():
        return user_controller.list_users()

    return admin_bp
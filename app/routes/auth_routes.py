from flask import Blueprint
from app.controllers.auth_controller import AuthController
from flask_login import login_required
from app.utils.decorators import admin_required

def create_auth_blueprint(auth_controller):
    auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

    @auth_bp.route('/user/login', methods=['GET', 'POST'])
    def login_user():
        return auth_controller.login_user()
    
    @auth_bp.route('/admin/login', methods=['GET', 'POST'])
    def login_admin():
        return auth_controller.login_admin()

    @auth_bp.route('/logout', methods=['GET'])
    @login_required
    def logout():
        return auth_controller.logout()

    return auth_bp
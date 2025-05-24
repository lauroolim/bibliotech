from flask import Blueprint
from app.controllers.auth_controller import AuthController
from flask_login import login_required

def create_auth_blueprint(auth_controller):
    auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

    @auth_bp.route('/user/login', methods=['GET', 'POST'])
    def login():
        return auth_controller.login_user()

    @auth_bp.route('/user/register', methods=['GET', 'POST'])
    def register():
        return auth_controller.register_user()

    @auth_bp.route('/user/logout', methods=['GET'])
    @login_required
    def logout():
        return auth_controller.logout_user()

    return auth_bp
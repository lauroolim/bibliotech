from flask import Blueprint, request, jsonify
from flask_login import login_required

def create_user_blueprint(user_controller, profile_controller):
    user_bp = Blueprint('user', __name__, url_prefix='/users')

    @user_bp.route('/', methods=['GET'])
    @login_required
    def profile():
        return profile_controller.show_profile()

    @user_bp.route('/update', methods=['POST'])
    @login_required
    def update_profile():
        return profile_controller.update_profile()

    @user_bp.route('/change-password', methods=['POST'])
    @login_required
    def change_password():
        return profile_controller.change_password()

    @user_bp.route('/deactivate', methods=['POST'])
    @login_required
    def deactivate_account():
        return profile_controller.deactivate_account()

    @user_bp.route('/search', methods=['GET'])
    @login_required
    def search_user_ajax():
        return user_controller.search_user_ajax()

    return user_bp

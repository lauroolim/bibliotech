from flask import Blueprint, request, jsonify
from flask_login import login_required

def create_user_blueprint(user_controller):
    user_bp = Blueprint('user', __name__, url_prefix='/users')

    @user_bp.route('/search', methods=['GET'])
    @login_required
    def search_user_ajax():
        return user_controller.search_user_ajax()

    return user_bp

from flask import Blueprint
from flask_login import login_required

def create_profile_blueprint(profile_controller):
    profile_bp = Blueprint('user', __name__, url_prefix='/profile')

    @profile_bp.route('/', methods=['GET'])
    @login_required
    def profile():
        return profile_controller.show_profile()

    @profile_bp.route('/update', methods=['POST'])
    @login_required
    def update_profile():
        return profile_controller.update_profile()

    @profile_bp.route('/change-password', methods=['POST'])
    @login_required
    def change_password():
        return profile_controller.change_password()

    @profile_bp.route('/deactivate', methods=['POST'])
    @login_required
    def deactivate_account():
        return profile_controller.deactivate_account()

    return profile_bp
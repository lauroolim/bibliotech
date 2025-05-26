from flask import Blueprint
from flask_login import login_required
from app.utils.decorators import admin_required

def create_admin_blueprint(user_controller, book_controller, admin_controller, loan_controller):
    admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


    @admin_bp.route('/dashboard', methods=['GET'])
    @login_required
    @admin_required
    def dashboard():
        return admin_controller.show_dashboard()

    # users
    @admin_bp.route('/users/register', methods=['GET', 'POST'])
    @login_required
    @admin_required
    def register_user():
        return user_controller.register_user()

    @admin_bp.route('/users/list', methods=['GET'])
    @login_required
    @admin_required
    def list_users():
        return user_controller.list_users()

    # Livros
    @admin_bp.route('/books/register', methods=['GET', 'POST'])
    @login_required
    @admin_required
    def register_book():
        return book_controller.register_book()
    
    @admin_bp.route('/books/author/register', methods=['GET', 'POST'])
    @login_required
    @admin_required
    def register_author():
        return book_controller.register_author()

    @admin_bp.route('/books/list', methods=['GET'])
    @login_required
    @admin_required
    def list_books():
        return book_controller.list_books()

    # emprestimos
    @admin_bp.route('/loans', methods=['GET'])
    @login_required
    @admin_required
    def list_loans():
        return loan_controller.list_loans()

    @admin_bp.route('/loans/register', methods=['GET', 'POST'])
    @login_required
    @admin_required
    def register_loan():
        return loan_controller.register_loan()

    @admin_bp.route('/loans/<int:loan_id>/return', methods=['GET', 'POST'])
    @login_required
    @admin_required
    def return_loan(loan_id):
        return loan_controller.return_loan(loan_id)

    @admin_bp.route('/loans/<int:loan_id>', methods=['GET'])
    @login_required
    @admin_required
    def view_loan(loan_id):
        return loan_controller.view_loan(loan_id)

    @admin_bp.route('/loans/overdue', methods=['GET'])
    @login_required
    @admin_required
    def overdue_loans():
        return loan_controller.overdue_loans()

    #AJAX para busca
    @admin_bp.route('/api/search-user', methods=['GET'])
    @login_required
    @admin_required
    def search_user_ajax():
        return loan_controller.search_user_ajax()

    @admin_bp.route('/api/search-book', methods=['GET'])
    @login_required
    @admin_required
    def search_book_ajax():
        return loan_controller.search_book_ajax()

    @admin_bp.route('/api/check-book-availability', methods=['GET'])
    @login_required
    @admin_required
    def check_book_availability():
        return loan_controller.check_book_availability_ajax()

    return admin_bp
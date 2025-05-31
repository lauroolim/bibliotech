from flask import Blueprint, request, jsonify
from flask_login import login_required

def create_book_blueprint(book_controller):
    book_bp = Blueprint('book', __name__, url_prefix='/books')

    @book_bp.route('/search', methods=['GET'])
    @login_required
    def search_book_ajax():
        return book_controller.search_book_by_isbn_ajax()

    return book_bp
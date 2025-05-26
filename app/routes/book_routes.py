from flask import Blueprint, request, jsonify

def create_book_blueprint(book_controller):
    book_bp = Blueprint('book', __name__, url_prefix='/api/books')

    @book_bp.route('/search', methods=['GET'])
    def search_book_ajax():
        term = request.args.get('term', '').strip()
        if not term:
            return jsonify({'error': 'Termo de busca é obrigatório'}), 400
        
        try:
            book = book_controller.search_book_by_isbn(term)
            return jsonify({
                'id': book.id,
                'title': book.title,
                'isbn': book.isbn,
                'author': book.author.name if hasattr(book, 'author') and book.author else 'N/A',
                'publication_year': book.publish_year or 'N/A',
                'available': getattr(book, 'is_available', True)
            })
        except ValueError as e:
            return jsonify({'error': str(e)}), 404

    return book_bp
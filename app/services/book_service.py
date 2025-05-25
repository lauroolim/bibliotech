from app.repositories.book_repository import IBookRepository
from app.models.book import Book


class BookService:
    def __init__(self, book_repository: IBookRepository):
        self.book_repository = book_repository

    def register_book(self, title, isbn, publish_year=None, author_ids=None):
        if self.book_repository.fetch_book_by_isbn(isbn):
            raise ValueError("ISBN já cadastrado")

        book_id = self.book_repository.insert_book(title, isbn, publish_year)
        if not book_id:
            raise ValueError("falha no cadastro do livro")

        if author_ids:
            for author_id in author_ids:
                if not self.book_repository.associate_book_author(book_id, author_id):
                    raise ValueError(f"erro ao associar autor {author_id} ao livro")

        return book_id

    def get_all_authors(self):
        return self.book_repository.fetch_all_authors()

    def register_author(self, full_name):
        if not full_name or not full_name.strip():
            raise ValueError("Nome do autor é obrigatório")

        if not self.book_repository.insert_author(full_name.strip()):
            raise ValueError("falha ao no service de cadastrar autor")

    def list_books(self, page=1, per_page=10):
        books = self.book_repository.fetch_all_books(page, per_page)
        
        total_count = self.book_repository.count_books()
        total_pages = (total_count + per_page - 1) // per_page
        
        return {
            'books': books,
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages,
            'total_count': total_count,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }
    

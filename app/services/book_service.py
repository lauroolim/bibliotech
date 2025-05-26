from app.repositories.book_repository import IBookRepository
from app.repositories.loan_repository import ILoanRepository
import logging

logger = logging.getLogger(__name__)

class BookService:
    def __init__(self, book_repository: IBookRepository, loan_repository: ILoanRepository = None):
        self.book_repository = book_repository
        self.loan_repository = loan_repository

    def register_book(self, title, isbn, publish_year=None, author_ids=None):
        if not title or not title.strip():
            raise ValueError("Titulo obrigatorio")
        
        if not isbn or not isbn.strip():
            raise ValueError("ISBN é obrigatório")

        if self.book_repository.fetch_book_by_isbn(isbn):
            raise ValueError("ISBN ja cadastrado")

        book_id = self.book_repository.insert_book(title.strip(), isbn.strip(), publish_year)
        if not book_id:
            raise ValueError("Falha no cadastro do livro")

        logger.info(f"Livro criado com ID: {book_id}")

        if author_ids:
            self._associate_authors(book_id, author_ids)

        return book_id

    def register_author(self, full_name):
        if not full_name or not full_name.strip():
            raise ValueError("Nome do autor obrigatório")

        if not self.book_repository.insert_author(full_name.strip()):
            raise ValueError("Falha ao cadastrar autor")

    def get_all_authors(self):
        return self.book_repository.fetch_all_authors()

    def list_books(self, page=1, per_page=10, search=None):
        books = self.book_repository.fetch_all_books(page, per_page, search)
        total_count = self.book_repository.count_books(search) 
        total_pages = (total_count + per_page - 1) // per_page

        if self.loan_repository:
            for book in books:
                book.is_available = self.loan_repository.is_book_available(book.id)
        
        return {
            'books': books,
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages,
            'total_count': total_count,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }

    def _associate_authors(self, book_id, author_ids):
        for author_id in author_ids:
            try:
                author_id = int(author_id)
                
                if not self.book_repository.fetch_author_by_id(author_id):
                    raise ValueError(f"Autor com ID {author_id} nao encontrado")
                
                if not self.book_repository.associate_book_author(book_id, author_id):
                    raise ValueError(f"Erro ao associar autor {author_id} ao livro")
                    
                logger.info(f"Autor {author_id} associado ao livro {book_id}")
                
            except ValueError as e:
                if "invalid literal" in str(e):
                    raise ValueError(f"ID do autor inválido: {author_id}")
                raise e
            except Exception as e:
                logger.error(f"erro inesperado ao associar autor {author_id}: {str(e)}")
                raise ValueError(f"erro ao associar autor {author_id} ao livro")
        
    def search_by_isbn(self, isbn):
        if not isbn or not isbn.strip():
            raise ValueError("ISBN é obrigatório")
        
        book = self.book_repository.fetch_book_by_isbn(isbn.strip())
        if not book:
            raise ValueError(f"Livro com ISBN {isbn} não encontrado")
        
        book.authors = self.book_repository._fetch_authors_by_book_id(book.id)
        
        if self.loan_repository:
            book.is_available = self.loan_repository.is_book_available(book.id)
            book.available_copies = 1 if book.is_available else 0
            book.total_copies = 1
        else:
            book.is_available = True
            book.available_copies = 1
            book.total_copies = 1
        
        return book

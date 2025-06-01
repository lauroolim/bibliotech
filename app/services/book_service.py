from app.repositories.book_repository import IBookRepository
import logging
logger = logging.getLogger(__name__)

class BookService:
    def __init__(self, book_repository: IBookRepository):
        self.book_repository = book_repository
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

        for book in books:
            book.is_available = self.book_repository.is_book_available(book.id)
        
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
                    
                #logger.info(f"Autor {author_id} associado ao livro {book_id}")
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
            raise ValueError(f"livro com ISBN {isbn} não encontrado")
        
        book.authors = self.book_repository._fetch_authors_by_book_id(book.id)
        book.is_available = self.book_repository.is_book_available(book.id)
        book.available_copies = 1 if book.is_available else 0
        book.total_copies = 1
        
        return book

    def get_book_by_id(self, book_id):
        book = self.book_repository.fetch_book_by_id(book_id)
        if not book:
            raise ValueError("Livro não encontrado")
        
        book.authors = self.book_repository._fetch_authors_by_book_id(book.id)
        book.is_available = self.book_repository.is_book_available(book.id)
        book.available_copies = 1 if book.is_available else 0
        book.total_copies = 1
        return book
    
    def update_book(self, book_id, title=None, isbn=None, publish_year=None, author_ids=None):
        if not book_id:
            raise ValueError("bookID obrigatorio")
        
        book = self.book_repository.fetch_book_by_id(book_id)
        if not book:
            raise ValueError("livro nao encontrado")

        if title:
            book.title = title.strip()
        if isbn:
            if not isbn.strip():
                raise ValueError("ISBN obrigatorio")
                
            existing_book = self.book_repository.fetch_book_by_isbn(isbn.strip())
            if existing_book and existing_book.id != book_id:
                raise ValueError("ISBN ja cadastrado")
            book.isbn = isbn.strip()
        if publish_year:
            try:
                book.publish_year = int(publish_year)
            except ValueError:
                raise ValueError("Ano de publicação inválido")
        
        book_updated = self.book_repository.update_book(
            book_id=book_id,
            title=book.title,
            isbn=book.isbn,
            publish_year=book.publish_year
        )
        if not book_updated:
            raise ValueError("falha ao atualizar livro")
        
        if author_ids is not None: 
            self._remove_all_book_authors(book_id)
            if author_ids:  
                self._associate_authors(book_id, author_ids)
            #logger.info(f"Autores do livro {book_id} atualizados: {len(author_ids)} autores associados")
        return book.id
    
    def delete_book(self, book_id):
        if not book_id:
            raise ValueError("bookID obrigatorio")
        
        book = self.book_repository.fetch_book_by_id(book_id)
        if not book:
            raise ValueError("livro nao encontrado")
        
        if not self.book_repository.delete_book(book_id):
            raise ValueError("Falha ao deletar livro")
        return True
    def _remove_all_book_authors(self, book_id):

        if not self.book_repository.remove_all_book_authors(book_id):
            logger.warning(f"Falha ao remover autores do livro {book_id}")

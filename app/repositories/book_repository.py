from abc import ABC, abstractmethod
from app.models.book import Book
import logging

logger = logging.getLogger(__name__)

class IBookRepository(ABC):
    @abstractmethod
    def insert_book(self, title: str, isbn: str, publish_year: int = None) -> int:
        pass

    @abstractmethod
    def fetch_book_by_isbn(self, isbn: str) -> Book:
        pass

    @abstractmethod
    def fetch_all_books(self, page: int, per_page: int) -> list[Book]:
        pass

    @abstractmethod
    def fetch_all_authors(self) -> list:
        pass

    @abstractmethod
    def insert_author(self, full_name: str) -> bool:
        pass

    @abstractmethod
    def associate_book_author(self, book_id: int, author_id: int) -> bool:
        pass

    @abstractmethod
    def count_books(self) -> int:
        pass


class PSQLBookRepository(IBookRepository):
    def __init__(self, db):
        self.db = db

    def insert_book(self, title: str, isbn: str, publish_year: int = None):
        query = "INSERT INTO bibliotech.books (title, isbn, publish_year) VALUES (?, ?, ?)"
        params = [title, isbn, publish_year]  

        try:
            self.db.execute_query(query, params)
            return True
        except Exception as e:
            logger.error(f"Erro ao inserir livro: {str(e)}")
            return False

    def fetch_book_by_isbn(self, isbn: str):
        query = "SELECT id, title, isbn, publish_year, created_at FROM bibliotech.books WHERE isbn = ?"
        params = [isbn]

        try:
            cursor = self.db.execute_query(query, params)
            book = cursor.fetchone()

            if book:
                return Book(
                    id=book[0], 
                    title=book[1], 
                    isbn=book[2], 
                    publish_year=book[3], 
                    created_at=book[4]
                )
            return None
        except Exception as e:
            logger.error(f"falha ao buscar livro por ISBN: {str(e)}")
            return None

    def fetch_all_books(self, page: int, per_page: int):
        offset = (page - 1) * per_page
        query = "SELECT DISTINCT b.id, b.title, b.isbn, b.publish_year, b.created_at FROM bibliotech.books b ORDER BY b.id LIMIT ? OFFSET ?"
        params = [per_page, offset]

        try:
            cursor = self.db.execute_query(query, params)
            books = cursor.fetchall()

            if books:
                books_with_authors = []
                for book in books:
                    authors = self._fetch_authors_by_book_id(book[0])
                    book_obj = Book(
                        id=book[0], 
                        title=book[1], 
                        isbn=book[2], 
                        publish_year=book[3], 
                        created_at=book[4],
                        authors=authors
                    )
                    books_with_authors.append(book_obj)
                return books_with_authors
            return []
        except Exception as e:
            logger.error(f"falha ao buscar todos os livros: {str(e)}")
            return []

    def count_books(self):
        query = "SELECT COUNT(*) FROM bibliotech.books"
        
        try:
            cursor = self.db.execute_query(query)
            result = cursor.fetchone()
            return result[0] if result else 0
        except Exception as e:
            logger.error(f"falha ao contar total de livros: {str(e)}")
            return 0

    def fetch_all_authors(self):
        query = "SELECT id, full_name FROM bibliotech.authors ORDER BY full_name"
        
        try:
            cursor = self.db.execute_query(query)
            authors = cursor.fetchall()
            return [{'id': author[0], 'full_name': author[1]} for author in authors]
        except Exception as e:
            logger.error(f"erro ao buscar autores: {str(e)}")
            return []
    
    def insert_author(self, full_name: str):
        query = "INSERT INTO bibliotech.authors (full_name) VALUES (?)"
        params = [full_name]

        try:
            self.db.execute_query(query, params)
            return True
        except Exception as e:
            logger.error(f"Erro ao inserir autor: {str(e)}")
            return False
    
    def associate_book_author(self, book_id: int, author_id: int):
        query = "INSERT INTO bibliotech.books_authors (book_id, author_id) VALUES (?, ?)"
        params = [book_id, author_id]

        try:
            self.db.execute_query(query, params)
            return True
        except Exception as e:
            logger.error(f"erro ao associar livro e autor: {str(e)}")
            return False
    
    def _fetch_authors_by_book_id(self, book_id):
        query = """
        SELECT a.id, a.full_name 
        FROM bibliotech.authors a
        INNER JOIN bibliotech.books_authors ba ON a.id = ba.author_id
        WHERE ba.book_id = ?
        ORDER BY a.full_name
        """
        params = [book_id]

        try:
            cursor = self.db.execute_query(query, params)
            authors = cursor.fetchall()
            return [{'id': author[0], 'full_name': author[1]} for author in authors]
        except Exception as e:
            logger.error(f"falha ao buscar autores do livro {book_id}: {str(e)}")
            return []
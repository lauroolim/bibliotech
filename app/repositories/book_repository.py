from abc import ABC, abstractmethod
from app.models.book import Book
import logging

logger = logging.getLogger(__name__)

class IBookRepository(ABC):
    @abstractmethod
    def insert_book(self, title: str, isbn: str, publish_year: int = None) -> int:
        pass

    @abstractmethod
    def fetch_book_by_id(self, book_id: int) -> Book:
        pass

    @abstractmethod
    def fetch_book_by_isbn(self, isbn: str) -> Book:
        pass

    @abstractmethod
    def fetch_all_books(self, page: int, per_page: int) -> list[Book]:
        pass

    @abstractmethod
    def count_books(self) -> int:
        pass

    @abstractmethod
    def fetch_all_authors(self) -> list:
        pass

    @abstractmethod
    def insert_author(self, full_name: str) -> bool:
        pass

    @abstractmethod
    def fetch_author_by_id(self, author_id: int) -> dict:
        pass

    @abstractmethod
    def associate_book_author(self, book_id: int, author_id: int) -> bool:
        pass

    @abstractmethod
    def is_book_available(self, book_id: int) -> bool:
        pass

    @abstractmethod
    def update_book(self, book_id: int, title: str = None, isbn: str = None, publish_year: int = None) -> bool:
        pass
    
    @abstractmethod
    def delete_book(self, book_id: int) -> bool:
        pass 
class PSQLBookRepository(IBookRepository):
    def __init__(self, db):
        self.db = db

    def insert_book(self, title, isbn, publish_year=None):
        insert_query = "INSERT INTO books (title, isbn, publish_year) VALUES (?, ?, ?)"
        select_query = "SELECT id FROM books WHERE isbn = ?"
        insert_params = [title, isbn, publish_year]

        try:
            self.db.execute_query(insert_query, insert_params)
            cursor = self.db.execute_query(select_query, [isbn])
            result = cursor.fetchone()
            
            if result:
                #logger.info(f"Livro inserido com sucesso. ID: {result[0]}")
                return result[0]
            
            logger.error("Livro inserido mas ID não encontrado")
            return None
        except Exception as e:
            logger.error(f"Erro ao inserir livro: {str(e)}")
            return None

    def fetch_book_by_id(self, book_id):
        query = "SELECT id, title, isbn, publish_year, created_at FROM books WHERE id = ?"
        params = [book_id]

        try:
            cursor = self.db.execute_query(query, params)
            book = cursor.fetchone()

            if book:
                authors = self._fetch_authors_by_book_id(book[0])
                return Book(
                    id=book[0], 
                    title=book[1], 
                    isbn=book[2], 
                    publish_year=book[3], 
                    created_at=book[4],
                    authors=authors
                )
            return None
        except Exception as e:
            logger.error(f"Falha ao buscar livro por ID: {str(e)}")
            return None

    def fetch_book_by_isbn(self, isbn):
        query = "SELECT id, title, isbn, publish_year, created_at FROM books WHERE isbn = ?"
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
            logger.error(f"Falha ao buscar livro por ISBN: {str(e)}")
            return None

    def fetch_all_books(self, page, per_page, search=None):
        offset = (page - 1) * per_page
        query = "SELECT id, title, isbn, publish_year, created_at FROM books ORDER BY id LIMIT ? OFFSET ?"
        params = [per_page, offset]

        if search:
            query = "SELECT id, title, isbn, publish_year, created_at FROM books WHERE title LIKE ? OR isbn LIKE ? ORDER BY id LIMIT ? OFFSET ?"
            search_param = f"%{search}%"
            params = [search_param, search_param, per_page, offset]
        else:
            query = "SELECT id, title, isbn, publish_year, created_at FROM books ORDER BY id LIMIT ? OFFSET ?"
            params = [per_page, offset]

        try:
            cursor = self.db.execute_query(query, params)
            books = cursor.fetchall()

            if books:
                return [
                    Book(
                        id=book[0], 
                        title=book[1], 
                        isbn=book[2], 
                        publish_year=book[3], 
                        created_at=book[4],
                        authors=self._fetch_authors_by_book_id(book[0])
                    ) for book in books
                ]
            return []
        except Exception as e:
            logger.error(f"Falha ao buscar todos os livros: {str(e)}")
            return []

    def count_books(self, search=None):
        if search:
            query = "SELECT COUNT(*) FROM books WHERE title LIKE ? OR isbn LIKE ?"
            search_param = f"%{search}%"
            params = [search_param, search_param]
        else:
            query = "SELECT COUNT(*) FROM books"
            params = []
        
        try:
            cursor = self.db.execute_query(query, params)
            result = cursor.fetchone()
            return result[0] if result else 0
        except Exception as e:
            logger.error(f"Falha ao contar total de livros: {str(e)}")
            return 0
            
    def fetch_all_authors(self):
        query = "SELECT id, full_name FROM authors ORDER BY full_name"
        
        try:
            cursor = self.db.execute_query(query)
            authors = cursor.fetchall()
            return [{'id': author[0], 'full_name': author[1]} for author in authors]
        except Exception as e:
            logger.error(f"Erro ao buscar autores: {str(e)}")
            return []
    
    def insert_author(self, full_name):
        query = "INSERT INTO authors (full_name) VALUES (?)"
        params = [full_name]

        try:
            self.db.execute_query(query, params)
            return True
        except Exception as e:
            logger.error(f"Erro ao inserir autor: {str(e)}")
            return False

    def fetch_author_by_id(self, author_id):
        query = "SELECT id, full_name FROM authors WHERE id = ?"
        params = [author_id]

        try:
            cursor = self.db.execute_query(query, params)
            author = cursor.fetchone()
            return {'id': author[0], 'full_name': author[1]} if author else None
        except Exception as e:
            logger.error(f"Falha ao buscar autor por ID: {str(e)}")
            return None
    
    def associate_book_author(self, book_id, author_id):
        check_query = "SELECT COUNT(*) FROM books_authors WHERE book_id = ? AND author_id = ?"
        
        try:
            cursor = self.db.execute_query(check_query, [book_id, author_id])
            result = cursor.fetchone()
            
            if result and result[0] > 0:
                logger.warning(f"Associação já existe: livro {book_id} com autor {author_id}")
                return True
        except Exception as e:
            logger.error(f"Erro ao verificar associação: {str(e)}")

        insert_query = "INSERT INTO books_authors (book_id, author_id) VALUES (?, ?)"
        
        try:
            self.db.execute_query(insert_query, [book_id, author_id])
            #logger.info(f"Associação criada: livro {book_id} com autor {author_id}")
            return True
        except Exception as e:
            logger.error(f"Erro ao associar livro {book_id} e autor {author_id}: {str(e)}")
            return False
    
    def _fetch_authors_by_book_id(self, book_id):
        query = """
        SELECT a.id, a.full_name 
        FROM authors a
        INNER JOIN books_authors ba ON a.id = ba.author_id
        WHERE ba.book_id = ?
        ORDER BY a.full_name
        """
        params = [book_id]

        try:
            cursor = self.db.execute_query(query, params)
            authors = cursor.fetchall()
            return [{'id': author[0], 'full_name': author[1]} for author in authors]
        except Exception as e:
            logger.error(f"Falha ao buscar autores do livro {book_id}: {str(e)}")
            return []

    def is_book_available(self, book_id):
        query = "SELECT COUNT(*) FROM loans WHERE book_id = ? AND returned_at IS NULL"
        params = [book_id]

        try:
            cursor = self.db.execute_query(query, params)
            result = cursor.fetchone()
            count = result[0] if result else 0
            return count == 0
        except Exception as e:
            logger.error(f"Erro ao verificar disponibilidade do livro: {str(e)}")
            return False
    
    def update_book(self, book_id: int, title: str = None, isbn: str = None, publish_year: int = None):
        query = "UPDATE books SET title = ?, isbn = ?, publish_year = ? WHERE id = ?"
        params = [title, isbn, publish_year, book_id]

        try:
            self.db.execute_query(query, params)
            return True
        except Exception as e:
            logger.error(f"falha ao atualizar book no banco: {str(e)}")
            return False

    def delete_book(self, book_id: int):
        try:
            delete_associations_query = "DELETE FROM books_authors WHERE book_id = ?"
            self.db.execute_query(delete_associations_query, [book_id])
            
            delete_book_query = "DELETE FROM books WHERE id = ?"
            self.db.execute_query(delete_book_query, [book_id])
            
            #logger.info(f"Livro {book_id} e suas associações deletados com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro ao deletar livro {book_id}: {str(e)}")
            return False
            
from abc import ABC, abstractmethod
from app.models.loan import Loan
from app.models.book import Book
from app.models.user import User
from app.models.employee import Employee
import logging
from datetime import date, datetime, timedelta

logger = logging.getLogger(__name__)

class ILoanRepository(ABC):
    @abstractmethod
    def insert_loan(self, user_id: int, book_id: int, employee_id: int, expected_return_date: date) -> int:
        pass

    @abstractmethod
    def fetch_loan_by_id(self, loan_id: int) -> Loan:
        pass

    @abstractmethod
    def is_book_available(self, book_id: int) -> bool:
        pass

    @abstractmethod
    def fetch_all_loans(self, page: int, per_page: int, status: str = None, search: str = None) -> list[Loan]:
        pass

    @abstractmethod
    def update_loan_return(self, loan_id: int, return_date: date, notes: str = None) -> bool:
        pass

    @abstractmethod
    def count_loans(self, status: str = None) -> int:
        pass

    @abstractmethod
    def fetch_overdue_loans(self) -> list[Loan]:
        pass

    @abstractmethod
    def fetch_loan_stats(self) -> dict:
        pass

class PSQLLoanRepository(ILoanRepository):
    def __init__(self, db):
        self.db = db

    def insert_loan(self, user_id, book_id, employee_id, expected_return_date: date):
        query = "INSERT INTO loans (user_id, book_id, employee_id, expected_return_date, created_at) VALUES (?, ?, ?, ?, ?) RETURNING id"
        params = [user_id, book_id, employee_id, expected_return_date, datetime.now()]

        try:
            logger.debug(f"Criando empréstimo: user={user_id}, book={book_id}, employee={employee_id}")
            cursor = self.db.execute_query(query, params)
            result = cursor.fetchone()
            cursor.close()
            
            loan_id = result[0] if result else None
            logger.info(f"Empréstimo criado com ID: {loan_id}")

            return loan_id
        except Exception as e:
            logger.error(f"Erro ao criar empréstimo: {str(e)}")
            return None

    def is_book_available(self, book_id):
        query = "SELECT COUNT(*) FROM loans WHERE book_id = ? AND returned_at IS NULL"
        params = [book_id]

        try:
            cursor = self.db.execute_query(query, params)
            result = cursor.fetchone()
            cursor.close()
            
            count = result[0] if result else 0
            return count == 0  
        except Exception as e:
            logger.error(f"falha ao verificar disponibilidade do livro {book_id}: {str(e)}")
            return False

    def fetch_loan_by_id(self, loan_id):
        query = """
        SELECT l.id, l.created_at, l.expected_return_date, l.returned_at, 
            l.user_id, l.book_id, l.employee_id,
            u.username, u.email,
            b.title, b.isbn,
            e.username as employee_name, e.email as employee_email, e.cpf as employee_cpf
        FROM loans l
        LEFT JOIN users u ON l.user_id = u.id
        LEFT JOIN books b ON l.book_id = b.id
        LEFT JOIN employees e ON l.employee_id = e.id
        WHERE l.id = ?
        """
        params = [loan_id]

        try:
            cursor = self.db.execute_query(query, params)
            loan_data = cursor.fetchone()

            if loan_data:
                status = self._determine_loan_status(loan_data[2], loan_data[3])
                
                user_obj = None
                if loan_data[7]:
                    user_obj = User(id=loan_data[4], username=loan_data[7], email=loan_data[8])
                
                book_obj = None
                if loan_data[9]:
                    book_obj = Book(id=loan_data[5], title=loan_data[9], isbn=loan_data[10])
                
                employee_obj = None
                if loan_data[11]:
                    employee_obj = Employee(
                        id=loan_data[6], 
                        username=loan_data[11], 
                        cpf=loan_data[12] or 'N/A',
                        email=loan_data[11]
                    )
                
                cursor.close()
                return Loan(
                    id=loan_data[0],
                    created_at=loan_data[1],
                    expected_return_date=loan_data[2],
                    returned_at=loan_data[3],
                    user_id=loan_data[4],
                    book_id=loan_data[5],
                    employee_id=loan_data[6],
                    status=status,
                    user=user_obj,
                    book=book_obj,
                    employee=employee_obj
                )
            cursor.close()
            return None
        except Exception as e:
            logger.error(f"Erro ao buscar empréstimo por ID: {str(e)}")
            return None

    def fetch_all_loans(self, page: int, per_page: int, status: str = None, search: str = None):
        offset = (page - 1) * per_page
        
        base_query = """
        SELECT l.id, l.created_at, l.expected_return_date, l.returned_at,
            l.user_id, l.book_id, l.employee_id,
            u.username, u.email,
            b.title, b.isbn,
            e.username as employee_name, e.email as employee_email, e.cpf as employee_cpf
        FROM loans l
        LEFT JOIN users u ON l.user_id = u.id
        LEFT JOIN books b ON l.book_id = b.id
        LEFT JOIN employees e ON l.employee_id = e.id
        WHERE 1=1
        """
        
        params = []
        if status:
            if status == 'ativo':
                base_query += " AND l.returned_at IS NULL AND l.expected_return_date >= CURRENT_DATE"
            elif status == 'encerrado':
                base_query += " AND l.returned_at IS NOT NULL"
            elif status == 'atrasado':
                base_query += " AND l.returned_at IS NULL AND l.expected_return_date < CURRENT_DATE"
        
        if search:
            base_query += " AND (u.username ILIKE ? OR u.email ILIKE ? OR b.title ILIKE ?)"
            search_param = f"%{search}%"
            params.extend([search_param, search_param, search_param])
        
        base_query += " ORDER BY l.created_at DESC LIMIT ? OFFSET ?"
        params.extend([per_page, offset])

        try:
            cursor = self.db.execute_query(base_query, params)
            loans_data = cursor.fetchall()
            
            loans = []
            for loan_data in loans_data:
                loan_status = self._determine_loan_status(loan_data[2], loan_data[3])
                
                user_obj = None
                if loan_data[7]:  
                    user_obj = User(id=loan_data[4], username=loan_data[7], email=loan_data[8])
                
                book_obj = None
                if loan_data[9]: 
                    book_obj = Book(id=loan_data[5], title=loan_data[9], isbn=loan_data[10])
                
                employee_obj = None
                if loan_data[11]: 
                    employee_obj = Employee(
                        id=loan_data[6], 
                        username=loan_data[11], 
                        cpf=loan_data[12] or 'N/A', 
                        email=loan_data[11] if len(loan_data) > 11 else None  
                    )
                
                loan = Loan(
                    id=loan_data[0],
                    created_at=loan_data[1],
                    expected_return_date=loan_data[2],
                    returned_at=loan_data[3],
                    user_id=loan_data[4],
                    book_id=loan_data[5],
                    employee_id=loan_data[6],
                    status=loan_status,
                    user=user_obj,
                    book=book_obj,
                    employee=employee_obj
                )
                loans.append(loan)
                
            cursor.close()
            return loans
            
        except Exception as e:
            logger.error(f"falha ao buscar emprestimos: {str(e)}")
            return []

    def update_loan_return(self, loan_id: int, return_date: date, notes: str = None):
        query = "UPDATE loans SET returned_at = ? WHERE id = ?"
        params = [return_date, loan_id]

        try:
            self.db.execute_query(query, params)
            return True
        except Exception as e:
            logger.error(f"falhou ao atualizar devolução: {str(e)}")
            return False

    def count_loans(self, status: str = None):
        base_query = "SELECT COUNT(*) FROM loans l WHERE 1=1"
        params = []

        if status:
            if status == 'ativo':
                base_query += " AND l.returned_at IS NULL AND l.expected_return_date >= CURRENT_DATE"
            elif status == 'encerrado':
                base_query += " AND l.returned_at IS NOT NULL"
            elif status == 'atrasado':
                base_query += " AND l.returned_at IS NULL AND l.expected_return_date < CURRENT_DATE"

        try:
            cursor = self.db.execute_query(base_query, params)
            result = cursor.fetchone()
            cursor.close()
            count = result[0] if result else 0
            return count
        except Exception as e:
            logger.error(f"falha ao contar empréstimos: {str(e)}")
            return 0

    def fetch_overdue_loans(self):
        today = date.today()
        query = """
        SELECT l.id, l.created_at, l.expected_return_date, l.returned_at,
               l.user_id, l.book_id, l.employee_id,
               u.username, u.email,
               b.title, b.isbn
        FROM loans l
        LEFT JOIN users u ON l.user_id = u.id
        LEFT JOIN books b ON l.book_id = b.id
        WHERE l.returned_at IS NULL AND l.expected_return_date < ?
        ORDER BY l.expected_return_date
        """
        params = [today]

        try:
            cursor = self.db.execute_query(query, params)
            loans_data = cursor.fetchall()

            loans = []
            for loan_data in loans_data:
                loan = Loan(
                    id=loan_data[0],
                    created_at=loan_data[1],
                    expected_return_date=loan_data[2],
                    returned_at=loan_data[3],
                    user_id=loan_data[4],
                    book_id=loan_data[5],
                    employee_id=loan_data[6],
                    status='atrasado',
                    user=User(id=loan_data[4], username=loan_data[7], email=loan_data[8]) if loan_data[7] else None,
                    book=Book(id=loan_data[5], title=loan_data[9], isbn=loan_data[10]) if loan_data[9] else None
                )
                loans.append(loan)
                
            cursor.close()
            return loans
        except Exception as e:
            logger.error(f"falha ao buscar empréstimos em atraso: {str(e)}")
            return []

    def fetch_loan_stats(self):
        today = date.today()
        
        queries = {
            'active_loans': "SELECT COUNT(*) FROM loans WHERE returned_at IS NULL",
            'overdue_loans': "SELECT COUNT(*) FROM loans WHERE returned_at IS NULL AND expected_return_date < ?",
            'returned_today': "SELECT COUNT(*) FROM loans WHERE DATE(returned_at) = ?",
            'monthly_loans': "SELECT COUNT(*) FROM loans WHERE EXTRACT(MONTH FROM created_at) = ? AND EXTRACT(YEAR FROM created_at) = ?"
        }

        stats = {}
        try:
            cursor = self.db.execute_query(queries['active_loans'])
            stats['active_loans'] = cursor.fetchone()[0]
            cursor.close()

            cursor = self.db.execute_query(queries['overdue_loans'], [today])
            stats['overdue_loans'] = cursor.fetchone()[0]
            cursor.close()

            cursor = self.db.execute_query(queries['returned_today'], [today])
            stats['returned_today'] = cursor.fetchone()[0]
            cursor.close()

            cursor = self.db.execute_query(queries['monthly_loans'], [today.month, today.year])
            stats['monthly_loans'] = cursor.fetchone()[0]
            cursor.close()

            return stats
        except Exception as e:
            logger.error(f"repository falhou ao buscar estatisticas de emprestimo: {str(e)}")
            return {'active_loans': 0, 'overdue_loans': 0, 'returned_today': 0, 'monthly_loans': 0}

    def _determine_loan_status(self, expected_return_date, returned_at):
        if returned_at:
            return 'encerrado'
        elif date.today() > expected_return_date:
            return 'atrasado'
        else:
            return 'ativo'
from app.repositories.loan_repository import ILoanRepository
from app.repositories.user_repository import IUserRepository
from app.repositories.book_repository import IBookRepository
from datetime import date, timedelta
import logging

logger = logging.getLogger(__name__)

class LoanService:
    def __init__(self, loan_repository: ILoanRepository, user_repository: IUserRepository, book_repository: IBookRepository):
        self.loan_repository = loan_repository
        self.user_repository = user_repository
        self.book_repository = book_repository

    def create_loan(self, user_id, book_id, employee_id, days_to_return = 14):
        if days_to_return < 0:
            raise ValueError("não é possível criar um emprestimo com dias antes da data atual")

        user = self.user_repository.fetch_user_by_id(user_id)
        if not user:
            raise ValueError("user nao encontrado")

        book = self.book_repository.fetch_book_by_id(book_id)
        if not book:
            raise ValueError("livro nao encontrado")
        expected_return_date = date.today() + timedelta(days=days_to_return)

        loan_id = self.loan_repository.insert_loan(user_id, book_id, employee_id, expected_return_date)
        logger.info(f"emprestimo criado: ID={loan_id}, User={user_id}, Book={book_id}")
        return loan_id
        

    def check_book_availability(self, book_id: int):
        is_available = self.book_repository.is_book_available(book_id)
        
        result = {
            'available': is_available,
            'book_id': book_id
        }
        
        if not is_available:
            loans = self.loan_repository.fetch_all_loans(1, 1, status='ativo')
            active_loan = None
            for loan in loans:
                if loan.book_id == book_id:
                    active_loan = loan
                    break
            
            if active_loan:
                result.update({
                    'loan_id': active_loan.id,
                    'borrower': active_loan.user.username if active_loan.user else 'N/A',
                    'due_date': active_loan.expected_return_date.isoformat(),
                    'is_overdue': active_loan.days_overdue() > 0,
                    'days_overdue': active_loan.days_overdue()
                })
        
        return result

    def return_loan(self, loan_id: int, return_date: date = None, notes: str = None):
        if not return_date:
            return_date = date.today()

        loan = self.loan_repository.fetch_loan_by_id(loan_id)
        if not loan:
            raise ValueError("Emprestimo nao encontrado")

        if loan.returned_at:
            raise ValueError("Emprestimo ja foi devolvido")

        if not self.loan_repository.update_loan_return(loan_id, return_date, notes):
            raise ValueError("Erro ao processar devolucao")

        fine_amount = 0
        if return_date > loan.expected_return_date:
            days_overdue = (return_date - loan.expected_return_date).days
            fine_amount = days_overdue * 2.00  

        return {
            'loan_id': loan_id,
            'fine_amount': fine_amount,
            'days_overdue': max(0, (return_date - loan.expected_return_date).days)
        }

    def list_loans(self, page: int = 1, per_page: int = 10, status: str = None, search: str = None):
        loans = self.loan_repository.fetch_all_loans(page, per_page, status, search)
        total_count = self.loan_repository.count_loans(status)
        total_pages = (total_count + per_page - 1) // per_page

        return {
            'loans': loans,
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages,
            'total_count': total_count,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }

    def get_loan_by_id(self, loan_id):
        loan = self.loan_repository.fetch_loan_by_id(loan_id)
        if not loan:
            raise ValueError("emprestimo não encontrado")
        return loan

    def get_overdue_loans(self):
        return self.loan_repository.fetch_overdue_loans()

    def get_dashboard_stats(self):
        return self.loan_repository.fetch_loan_stats()


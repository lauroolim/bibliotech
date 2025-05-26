from app.services.loan_service import LoanService
from app.repositories.loan_repository import ILoanRepository
from app.repositories.user_repository import IUserRepository  
from app.repositories.book_repository import IBookRepository
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import current_user
from datetime import date, timedelta
import logging

logger = logging.getLogger(__name__)

class LoanController:
    def __init__(self, loan_repository: ILoanRepository, user_repository: IUserRepository, book_repository: IBookRepository):
        self.loan_repository = loan_repository
        self.user_repository = user_repository
        self.book_repository = book_repository
        self.loan_service = LoanService(loan_repository, user_repository, book_repository)

    def list_loans(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status', '')
        search = request.args.get('search', '')

        logger.debug(f"Listando empréstimos - page: {page}, per_page: {per_page}, status: '{status}', search: '{search}'")

        try:
            pagination = self.loan_service.list_loans(
                page=page, 
                per_page=per_page, 
                status=status if status else None,
                search=search if search else None
            )
            
            #logger.debug(f"Resultado: {len(pagination['loans'])} empréstimos encontrados")
            #logger.debug(f"Paginação: {pagination}")
            
            return render_template('admin/list_loans.html', **pagination)
        except ValueError as e:
            flash(str(e), 'danger')
            return redirect(url_for('admin.dashboard'))

    def check_book_availability_ajax(self):
        book_id = request.args.get('book_id', type=int)
        if not book_id:
            return jsonify({'error': 'ID do livro obrigatório'}), 400

        try:
            availability = self.loan_service.check_book_availability(book_id)
            return jsonify(availability)
        except Exception as e:
            logger.error(f"falha ao verificar disponibilidade: {str(e)}")
            return jsonify({'error': 'Erro interno'}), 500

    def register_loan(self):
        if request.method == 'POST':
            try:
                user_id = int(request.form['user_id'])
                book_id = int(request.form['book_id'])
                expected_return_date = request.form['expected_return_date']
                
                return_date = date.fromisoformat(expected_return_date)
                days_to_return = (return_date - date.today()).days
                
                employee_id = current_user.id
                
                loan_id = self.loan_service.create_loan(
                    user_id=user_id,
                    book_id=book_id,
                    employee_id=employee_id,
                    days_to_return=days_to_return
                )
                
                flash(f'Empréstimo #{loan_id} criado!', 'success')
                return redirect(url_for('admin.list_loans'))
                
            except ValueError as e:
                flash(str(e), 'danger')
            except Exception as e:
                logger.error(f"falha ao criar empréstimo: {str(e)}")
                flash('Erro interno, tente novamente', 'danger')

        return render_template('admin/register_loan.html')


    def return_loan(self, loan_id):
        try:
            loan = self.loan_service.get_loan_by_id(loan_id)
        except ValueError as e:
            flash(str(e), 'danger')
            return redirect(url_for('admin.list_loans'))

        if request.method == 'POST':
            try:
                return_date_str = request.form['return_date']
                return_date = date.fromisoformat(return_date_str)
                notes = request.form.get('return_notes', '')
                
                result = self.loan_service.return_loan(
                    loan_id=loan_id,
                    return_date=return_date,
                    notes=notes
                )
                
                message = f'Devolução processada!'
                if result['fine_amount'] > 0:
                    message += f' Multa aplicada: R$ {result["fine_amount"]:.2f}'
                
                flash(message, 'success')
                return redirect(url_for('admin.list_loans'))
                
            except ValueError as e:
                flash(str(e), 'danger')
            except Exception as e:
                logger.error(f"falha ao processar devolução: {str(e)}")
                flash('Erro interno, tente novamente', 'danger')

        today = date.today().isoformat()
        return render_template('admin/return_loan.html', loan=loan, today=today)

    def view_loan(self, loan_id):
        try:
            loan = self.loan_service.get_loan_by_id(loan_id)
            return render_template('admin/view_loan.html', loan=loan)
        except ValueError as e:
            flash(str(e), 'danger')
            return redirect(url_for('admin.list_loans'))

    def search_user_ajax(self):
        search_term = request.args.get('term', '')
        if not search_term:
            return jsonify({'error': 'Termo de busca obrigatorio'}), 400

        try:
            user = self.loan_service.search_user(search_term)
            if user:
                return jsonify({
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                })
            else:
                return jsonify({'error': 'user não encontrado'}), 404
        except Exception as e:
            logger.error(f"falha ao busca de user: {str(e)}")
            return jsonify({'error': 'Erro interno'}), 500

    def search_book_ajax(self):
        search_term = request.args.get('term', '')
        if not search_term:
            return jsonify({'error': 'Termo de busca obrigatório'}), 400

        try:
            book = self.loan_service.search_book(search_term)
            if book:
                return jsonify({
                    'id': book.id,
                    'title': book.title,
                    'isbn': book.isbn
                })
            else:
                return jsonify({'error': 'Livro não encontrado'}), 404
        except Exception as e:
            logger.error(f"falha ao busca de livro: {str(e)}")
            return jsonify({'error': 'Erro interno'}), 500

    def overdue_loans(self):
        try:
            loans = self.loan_service.get_overdue_loans()
            return render_template('admin/overdue_loans.html', loans=loans)
        except Exception as e:
            logger.error(f"falha ao buscar emprestimos em atraso: {str(e)}")
            flash('Erro ao carregar empréstimos em atraso', 'danger')
            return redirect(url_for('admin.dashboard'))
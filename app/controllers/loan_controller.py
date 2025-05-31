from app.services.loan_service import LoanService
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import current_user
from datetime import date, timedelta, datetime, timezone
import logging
import pytz 
from app.utils.decorators import handle_controller_errors

logger = logging.getLogger(__name__)

class LoanController:
    def __init__(self, loan_service: LoanService):
        self.loan_service = loan_service

    @handle_controller_errors('admin.list_loans')
    def list_loans(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status', '')
        search = request.args.get('search', '')

        pagination = self.loan_service.list_loans(
            page=page, 
            per_page=per_page, 
            status=status if status else None,
            search=search if search else None
        )
        
        return render_template('admin/list_loans.html', **pagination)

    @handle_controller_errors('admin.register_loan')
    def register_loan(self):
        if request.method == 'POST':
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

        return render_template('admin/register_loan.html')

    @handle_controller_errors('admin.list_loans')
    def return_loan(self, loan_id):
        loan = self.loan_service.get_loan_by_id(loan_id)

        if request.method == 'POST':
            return_date = self._get_brazil_date()
            notes = request.form['return_notes'].strip()
            
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

        today_datetime = self._get_brazil_datetime()
        return render_template('admin/return_loan.html', loan=loan, today=today_datetime)

    @handle_controller_errors('admin.list_loans')
    def view_loan(self, loan_id):
        loan = self.loan_service.get_loan_by_id(loan_id)
        return render_template('admin/view_loan.html', loan=loan)

    @handle_controller_errors('admin.overdue_loans')
    def overdue_loans(self):
        loans = self.loan_service.get_overdue_loans()
        return render_template('admin/overdue_loans.html', loans=loans)

    def check_book_availability_ajax(self):
        book_id = request.args.get('book_id', type=int)
        if not book_id:
            return jsonify({'error': 'ID do livro obrigatório'}), 400

        try:
            availability = self.loan_service.check_book_availability(book_id)
            return jsonify(availability)
        except Exception as e:
            logger.error(f"Falha ao verificar disponibilidade: {str(e)}")
            return jsonify({'error': 'Erro interno'}), 500

    def _get_brazil_date(self):
        brazil_tz = pytz.timezone('America/Sao_Paulo')
        return datetime.now(brazil_tz).date()

    def _get_brazil_datetime(self):
        brazil_offset = timezone(timedelta(hours=-3))
        return datetime.now(brazil_offset)
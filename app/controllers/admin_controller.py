from flask import render_template
from app.services.loan_service import LoanService

class AdminController:
    def __init__(self, loan_service: LoanService = None):
        self.loan_service = loan_service

    def show_dashboard(self):
        stats = {'active_loans': 0, 'overdue_loans': 0, 'returned_today': 0, 'monthly_loans': 0}
        
        if self.loan_service:
            try:
                stats = self.loan_service.get_dashboard_stats()
            except Exception as e:
                stats = {'active_loans': 0, 'overdue_loans': 0, 'returned_today': 0, 'monthly_loans': 0}
        
        return render_template('admin/dashboard.html', stats=stats)
from flask import render_template
from app.services.loan_service import LoanService
from app.utils.decorators import handle_controller_errors
import logging

logger = logging.getLogger(__name__)
class AdminController:
    def __init__(self, loan_service: LoanService):
        self.loan_service = loan_service

    @handle_controller_errors('admin.dashboard') 
    def show_dashboard(self): 
        stats = self.loan_service.get_dashboard_stats()
        return render_template('admin/dashboard.html', stats=stats)
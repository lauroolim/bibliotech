from app.services.user_service import UserService
from app.services.loan_service import LoanService
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, logout_user
import logging
from app.utils.decorators import handle_controller_errors
logger = logging.getLogger(__name__)

class ProfileController:
    def __init__(self, user_service: UserService, loan_service: LoanService):
        self.user_service = user_service
        self.loan_service = loan_service

    @handle_controller_errors('user.profile')
    def show_profile(self):
        profile_data = self.user_service.get_user_profile_data(current_user.id)
        active_loans_list = self.user_service.get_user_active_loans(current_user.id)
        
        formatted_loans = []
        for loan_data in active_loans_list:
            formatted_loan = {
                'id': loan_data['id'],
                'expected_return_date': loan_data['expected_return_date'],
                'created_at': loan_data['created_at'],
                'book': {'title': loan_data['book_title']}
            }
            formatted_loans.append(formatted_loan)
        
        return render_template('user/profile.html', 
                                user=profile_data['user'],                    
                                active_loans=profile_data['active_loans'],   
                                overdue_loans=profile_data['overdue_loans'], 
                                total_loans=profile_data['total_loans'],    
                                active_loans_list=formatted_loans,           
                                recent_loans=[])                                                         

    @handle_controller_errors('user.profile')
    def update_profile(self):
        if request.method == 'POST':
        
            username = request.form['username'].strip()
            email = request.form['email'].strip()
            phone = request.form['phone'].strip()
            
            self.user_service.update_user(user_id=current_user.id, username=username, email=email, phone=phone)
            flash('Perfil atualizado com sucesso!', 'success')
        
            return redirect(url_for('user.profile'))

        return render_template('user/update_profile.html')

    @handle_controller_errors('user.profile')
    def change_password(self):
        if request.method == 'POST':
            current_password = request.form['current_password']
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']
            
            if not all([current_password, new_password, confirm_password]):
                flash('Todos os campos são obrigatórios', 'danger')
                return redirect(url_for('user.profile'))
            
            if new_password != confirm_password:
                flash('Nova senha e confirmação não coincidem', 'danger')
                return redirect(url_for('user.profile'))
            
            if len(new_password) < 6:
                flash('Nova senha deve ter pelo menos 6 caracteres', 'danger')
                return redirect(url_for('user.profile'))
            
            self.user_service.change_password(
                user_id=current_user.id,
                current_password=current_password,
                new_password=new_password
            )
            flash('Senha alterada com sucesso!', 'success')
            return redirect(url_for('user.profile'))

        return render_template('user/change_password.html')

    @handle_controller_errors('index')
    def deactivate_account(self):
        if request.method == 'POST':
            password = request.form['password']
            
            if not password:
                flash('A senha é obrigatória para desativar conta', 'danger')
                return redirect(url_for('user.profile'))
        
            self.user_service.deactivate_user(current_user.id, password)
            
            flash('Conta desativada com sucesso', 'info')
            logout_user()
            return redirect(url_for('index')) 
        return render_template('user/deactivate_account.html')
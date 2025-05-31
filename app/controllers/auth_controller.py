from app.services.auth_service import AuthService
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from app.utils.decorators import handle_controller_errors
import logging
logger = logging.getLogger(__name__)

class AuthController:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service 
    @handle_controller_errors('auth.login_user')
    def login_user(self):
        if current_user.is_authenticated:
            return redirect(url_for('index'))

        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            user = self.auth_service.login_user(email, password)
            login_user(user)  
            flash('Logado com sucesso!', 'success') 
            return redirect(url_for('index'))
        return render_template('auth/login_user.html') 
    
    @handle_controller_errors('auth.login_admin')
    def login_admin(self):
        if current_user.is_authenticated:
            return redirect(url_for('admin.dashboard'))   

        if request.method == 'POST':
            cpf = request.form['cpf']
            password = request.form['password']

            admin = self.auth_service.login_employee(cpf, password)
            login_user(admin)  
            flash('Administrador logado com sucesso!', 'success')
            return redirect(url_for('admin.dashboard'))
                
        return render_template('auth/login_admin.html') 

    def logout(self):
        logout_user()   
        flash('Você saiu com sucesso.', 'info')
        return redirect(url_for('auth.login_user'))


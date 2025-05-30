from app.services.auth_service import AuthService
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user

class AuthController:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    def login_user(self):
        if current_user.is_authenticated:
            return redirect(url_for('index'))

        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            user = self.auth_service.login_user(email, password)

            if user:
                login_user(user)
                flash('Logado com sucesso!', 'success')
                return redirect(url_for('index'))
                
            flash('Email ou senha inválidos', 'danger')
                
        return render_template('auth/login_user.html')
    
    def login_admin(self):
        if current_user.is_authenticated:
            return redirect(url_for('index'))

        if request.method == 'POST':
            cpf = request.form['cpf']
            password = request.form['password']

            admin = self.auth_service.login_employee(cpf, password)

            if admin:
                login_user(admin)
                flash('Administrador logado com sucesso!', 'success')
                return redirect(url_for('admin.dashboard'))
                
            flash('CPF ou senha inválidos', 'danger')
                
        return render_template('auth/login_admin.html')

    def logout(self):
        logout_user()  
        flash('Você saiu com sucesso.', 'info')
        return redirect(url_for('auth.login_user'))
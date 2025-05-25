from app.services.auth_service import AuthService
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from app.repositories.user_repository import IUserRepository 

class AuthController:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
        self.auth_service = AuthService(user_repository)

    def login(self):
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
            
            employee = self.user_repository.fetch_employee_by_email(email)

            if employee:
                flash('Login realizado com sucesso!', 'success')
                login_user(employee)
                return redirect(url_for('index'))
                
            flash('Email ou senha inválidos', 'danger')
                
        return render_template('auth/login.html')

    def register_user(self):
        if current_user.is_authenticated:
            return redirect(url_for('index'))

        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']

            try:
                self.auth_service.register_user(username, password, email)
                flash('Usuario cadastrado com sucesso', 'success') 
                return redirect(url_for('auth.login'))
            except ValueError as e:
                flash(str(e), 'danger')

        return render_template('auth/register_user.html')

    def logout_user(self):
        logout_user()  
        flash('Você saiu com sucesso.', 'info')
        return redirect(url_for('auth.login'))
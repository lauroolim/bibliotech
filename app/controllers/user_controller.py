from app.services.user_service import UserService
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from app.repositories.user_repository import IUserRepository

class UserController:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
        self.user_service = UserService(user_repository)

    def register_user(self):
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']

            try:
                self.user_service.register_user(username, password, email)
                flash('Usuário cadastrado com sucesso', 'success') 
                return redirect(url_for('admin.register_user'))  
            except ValueError as e:
                flash(str(e), 'danger')

        return render_template('admin/register_user.html')  
    
    def list_users(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        try:
            pagination = self.user_service.list_users(page, per_page)
            return render_template('admin/list_users.html', **pagination)
        except ValueError as e:
            flash(str(e), 'danger')
            return redirect(url_for('admin.dashboard'))

    def delete_user(self, user_id):
        try:
            user = self.user_service.delete_user(user_id)

            flash('Usuário deletado com sucesso', 'success')
        except ValueError as e:
            flash(str(e), 'danger')

        return redirect(url_for('admin.list_user'))

    def edit_user(self, user_id):
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']

            try:
                self.user_service.update_user(user_id, username, email)
                flash('Usuário atualizado com sucesso', 'success')
                return redirect(url_for('admin.user_list'))
            except ValueError as e:
                flash(str(e), 'danger')

        return render_template('admin/edit_user.html', user=user)

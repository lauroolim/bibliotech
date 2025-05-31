from app.services.user_service import UserService
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from app.utils.decorators import handle_controller_errors
import logging
from flask import jsonify
logger = logging.getLogger(__name__)

class UserController:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    @handle_controller_errors('admin.register_user')  
    def register_user(self):
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            phone = request.form['phone']

            self.user_service.register_user(username, password, email, phone)
            flash('Usuário cadastrado com sucesso', 'success') 

            return redirect(url_for('admin.list_users'))  
        return render_template('admin/register_user.html')  
    
    @handle_controller_errors('admin.list_users')
    def list_users(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '', type=str)
        
        pagination = self.user_service.list_users(page, per_page, search)
        return render_template('admin/list_users.html', **pagination)

    @handle_controller_errors('admin.list_users')
    def delete_user(self, user_id):
        self.user_service.deactivate_user(user_id)  

        flash('Usuário deletado com sucesso', 'success') 

        return redirect(url_for('admin.list_users'))

    @handle_controller_errors('admin.list_users')
    def edit_user(self, user_id):
        user = self.user_service.get_user_by_id(user_id) 
        
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']

            self.user_service.update_user(user_id, username, email)
            flash('Usuário atualizado com sucesso', 'success')
            return redirect(url_for('admin.list_users'))  
        return render_template('admin/edit_user.html', user=user)

    def search_user_ajax(self):
        search_term = request.args.get('term', '')
        if not search_term:
            return jsonify({'error': 'Termo de busca obrigatório'}), 400

        try:
            user = self.user_service.search_user(search_term)
            if user:
                return jsonify({
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'phone': user.phone or ''
                })
            else:
                return jsonify({'error': 'Usuário não encontrado'}), 404

        except ValueError as e:

            return jsonify({'error': str(e)}), 400
        except Exception as e:
            logger.error(f"Falha na busca de usuário: {str(e)}")
            return jsonify({'error': 'Erro interno'}), 500

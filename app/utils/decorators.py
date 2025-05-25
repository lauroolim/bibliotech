from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user
from app.models.employee import Employee

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not isinstance(current_user, Employee):
            flash('Acesso restrito para admins', 'danger')
            return redirect(url_for('auth.login_admin'))
        return f(*args, **kwargs)
    return decorated_function
from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Acesso restrito para admins', 'danger')
            return redirect(url_for('auth.login_admin'))
        return f(*args, **kwargs)
    return decorated_function

def handle_controller_errors(fallback_route=''):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except ValueError as e:
                logger.warning(f"falha de validação em {func.__name__}: {str(e)}")
                flash(str(e), 'danger')
                return redirect(url_for(fallback_route))
            except Exception as e:
                logger.error(f"erro interno em {func.__name__}: {str(e)}", exc_info=True)
                flash('Erro interno, tente novamente', 'danger')
                return redirect(url_for(fallback_route))
        return wrapper
    return decorator
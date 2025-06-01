from functools import wraps
from flask import flash, redirect, url_for, request
from flask_login import current_user
import logging
import traceback
logger = logging.getLogger(__name__)

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
            user_id = getattr(current_user, 'id', 'anônimo') if current_user.is_authenticated else 'anônimo'
            endpoint = request.endpoint or 'desconhecido'
            method = request.method
            
            try:
                return func(self, *args, **kwargs)
                
            except ValueError as e:
                logger.warning(
                    f"VALIDAÇÃO: {func.__name__} | "
                    f"Usuário: {user_id} | "
                    f"Endpoint: {endpoint} ({method}) | "
                    f"Erro: {str(e)}"
                )
                flash(str(e), 'danger')
                return redirect(url_for(fallback_route))
                
            except PermissionError as e:
                logger.error(
                    f"PERMISSÃO: {func.__name__} | "
                    f"Usuário: {user_id} | "
                    f"Endpoint: {endpoint} | "
                    f"Erro: {str(e)}"
                )
                flash('Acesso negado', 'danger')
                return redirect(url_for(fallback_route))
            except Exception as e:
                error_type = e.__class__.__name__
                logger.error(
                    f"ERRO [{error_type}]: {func.__name__} | "
                    f"Usuário: {user_id} | "
                    f"Endpoint: {endpoint} ({method}) | "
                    f"Erro: {str(e)}",
                    exc_info=True
                )
                flash('Erro interno, tente novamente', 'danger')
                return redirect(url_for(fallback_route))
        return wrapper
    return decorator
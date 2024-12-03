from functools import wraps
from flask import redirect, url_for, session, flash

AUTH_SERVICE_URL = "http://127.0.0.1:5006"

def login_required(f):
    """로그인 상태 확인 데코레이터"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("로그인이 필요합니다.", "danger")
            return redirect(f"{AUTH_SERVICE_URL}/login?redirect_url={url_for('auth.login_callback', _external=True)}")
        return f(*args, **kwargs)
    return decorated_function

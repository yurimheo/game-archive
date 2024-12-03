from functools import wraps
from flask import redirect, url_for, session, flash
import requests

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


def get_username(user_id):
    """auth-service에서 사용자 이름 가져오기"""
    try:
        response = requests.get(f"{AUTH_SERVICE_URL}/user/{user_id}")
        if response.status_code == 200:
            data = response.json()
            return data.get("username", "알 수 없음")
    except requests.RequestException as e:
        print(f"Error fetching username for user_id {user_id}: {e}")
    return "알 수 없음"
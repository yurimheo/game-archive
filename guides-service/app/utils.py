from functools import wraps
from flask import redirect, url_for, session, flash, request, jsonify, g
import requests
import jwt as pyjwt
from functools import wraps


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

SECRET_KEY = "supersecretkey"

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None

        # Authorization 헤더에서 토큰 가져오기
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

        # Authorization 헤더에 토큰이 없으면 쿠키에서 가져오기
        if not token:
            token = request.cookies.get("access_token")

        if not token:
            return jsonify({"error": "Authorization token required"}), 401

        try:
            # JWT 디코딩
            decoded_token = pyjwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            g.user = {
                "user_id": decoded_token["user_id"],
                "username": decoded_token["username"]
            }  # 사용자 정보를 Flask의 g 객체에 저장
        except pyjwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except pyjwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated_function


# 서비스 간  인증 - 인증 확인 요청
# : 만약 서비스가 인증된 요청인지 확인해야 한다면, Auth Service에 해당 Access Token을 보내 검증하기
def verify_token(access_token):
    response = requests.post(
        f"{AUTH_SERVICE_URL}/verify",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    if response.status_code == 200:
        return response.json()  # 사용자 정보 반환
    return None
import os
from app import create_app
from app.views import auth_blueprint  # views.py를 import
from flask_session import Session
from app.models import init_db
from flask import Flask, g, request
import jwt as pyjwt
import redis

# Flask 앱 생성
app = create_app()

# 블루프린트 등록
app.register_blueprint(auth_blueprint)

# Secret Key 설정
SECRET_KEY = "supersecretkey"

@app.before_request
def load_logged_in_user():
    """
    요청 전에 JWT를 확인하고 사용자 정보를 g.user에 저장합니다.
    """
    token = request.cookies.get('access_token')  # 클라이언트에서 보낸 토큰
    g.user = None

    if token:
        try:
            # JWT 디코딩
            decoded_token = pyjwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            g.user = {
                "user_id": decoded_token.get("user_id"),
                "username": decoded_token.get("username"),
            }
        except pyjwt.ExpiredSignatureError:
            pass  # 토큰 만료시 g.user를 None으로 둠
        except pyjwt.InvalidTokenError:
            pass  # 유효하지 않은 토큰

@app.context_processor
def inject_user():
    """
    템플릿에 g.user를 user 변수로 전달합니다.
    """
    return {"user": g.user}

# Flask-Session 설정
app.config["SESSION_TYPE"] = "redis"  # 세션을 Redis로 설정
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_REDIS"] = redis.StrictRedis(host='redis', port=6379, db=0)
Session(app)

# 데이터베이스 초기화
init_db()

if __name__ == "__main__":
    print(app.url_map)  # URL 매핑 출력
    app.run(host="0.0.0.0", port=5006, debug=True)

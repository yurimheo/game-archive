import os
from app import create_app
from app.views import main_blueprint
from flask_session import Session
from flask import g, request
import redis
import jwt as pyjwt

# Flask 앱 생성
app = create_app()

# 블루프린트 등록
app.register_blueprint(main_blueprint)

# Secret Key 설정
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
app.secret_key = SECRET_KEY

# Flask-Session 설정
app.config["SESSION_TYPE"] = "redis"  # 세션을 Redis로 설정
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_REDIS"] = redis.StrictRedis(host='redis', port=6379, db=0)

Session(app)

# JWT 검증 로직
@app.before_request
def load_logged_in_user():
    """
    요청마다 JWT를 확인하고 사용자 정보를 g.user에 저장.
    """
    token = request.cookies.get("access_token")
    g.user = None  # 초기화

    if token:
        try:
            # JWT 디코딩
            decoded_token = pyjwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            g.user = {
                "user_id": decoded_token.get("user_id"),
                "username": decoded_token.get("username"),
            }
        except pyjwt.ExpiredSignatureError:
            print("Access token expired")
        except pyjwt.InvalidTokenError:
            print("Invalid token")

# 실행
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

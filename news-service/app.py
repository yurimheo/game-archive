from flask import Flask, g, request
from app.views import news_blueprint
from flask_session import Session
import redis
import os
from app.models import db_session
import jwt as pyjwt

def create_app():
    app = Flask(__name__,
                static_folder='app/static',
                template_folder='app/templates')

    # Flask 설정
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "supersecretkey")
    app.config["SESSION_TYPE"] = "redis"
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_USE_SIGNER"] = True
    app.config["SESSION_REDIS"] = redis.StrictRedis(host='redis', port=6379, db=0)

    # 블루프린트 등록
    app.register_blueprint(news_blueprint, url_prefix='/news')

    # JWT 인증 처리
    @app.before_request
    def load_logged_in_user():
        """
        요청마다 JWT를 확인하고 사용자 정보를 g.user에 저장합니다.
        """
        token = request.cookies.get("access_token")  # 쿠키에서 JWT 토큰 가져오기
        g.user = None  # 기본값 초기화

        if token:
            try:
                # JWT 디코딩
                decoded_token = pyjwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
                g.user = {
                    "user_id": decoded_token.get("user_id"),
                    "username": decoded_token.get("username"),
                }
                print(f"[DEBUG] Decoded User: {g.user}")  # 디버깅용
            except pyjwt.ExpiredSignatureError:
                print("[DEBUG] Access token expired")
            except pyjwt.InvalidTokenError as e:
                print(f"[DEBUG] Invalid token: {e}")
        else:
            print("[DEBUG] No token found")

    # 데이터베이스 세션 종료
    @app.teardown_appcontext
    def remove_db_session(exception=None):
        db_session.remove()

    # 컨텍스트 프로세서 추가
    @app.context_processor
    def inject_user():
        """
        템플릿에 `user`를 전달
        """
        return {"user": g.user}

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5004, debug=True)

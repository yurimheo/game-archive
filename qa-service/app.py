import os
from flask import Flask, g, request
from app import create_app
from app.views import qa_blueprint  # views.py를 import
from flask_session import Session
from app.models import init_db
import jwt as pyjwt

# Flask 앱 생성
app = create_app()

# Secret Key 설정
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default_secret_key")

# Flask-Session 설정
app.config["SESSION_TYPE"] = "filesystem"  # 세션을 파일 시스템에 저장
Session(app)

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
            decoded_token = pyjwt.decode(
                token,
                app.config["SECRET_KEY"],  # SECRET_KEY 가져오기
                algorithms=["HS256"]
            )
            g.user = {
                "user_id": decoded_token.get("user_id"),
                "username": decoded_token.get("username"),
            }
            print(f"[DEBUG] Decoded User: {g.user}")  # 디버깅용
        except pyjwt.ExpiredSignatureError:
            print("[DEBUG] Access token expired")
        except pyjwt.InvalidTokenError as e:
            print(f"[DEBUG] Invalid token: {e}")
        except Exception as e:
            print(f"[DEBUG] Unexpected error: {e}")
    else:
        print("[DEBUG] No token found")

# 템플릿에 `user` 변수 전달
@app.context_processor
def inject_user():
    """
    `g.user`를 템플릿에 `user`로 전달
    """
    return {"user": g.user}

# 블루프린트 등록
app.register_blueprint(qa_blueprint)

if __name__ == "__main__":
    print(app.url_map)  # URL 매핑 출력
    app.run(host="0.0.0.0", port=5005, debug=True)

from flask import Flask, g, request
from app import create_app
import jwt as pyjwt
import os

# Flask 애플리케이션 생성
app = create_app()

# 기본값을 포함한 SECRET_KEY 설정
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "supersecretkey")

# SECRET_KEY 유효성 확인
if not app.config["SECRET_KEY"]:
    raise RuntimeError("SECRET_KEY is not set. Please configure it.")

print(f"[INFO] SECRET_KEY is set to: {app.config['SECRET_KEY']}")

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5007, debug=True)

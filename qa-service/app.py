import os
from app import create_app
from views import qa_blueprint  # views.py를 import
from flask_session import Session
from models import init_db

# Flask 앱 생성
app = create_app()

# 블루프린트 등록
app.register_blueprint(qa_blueprint)

# Secret Key 설정
app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")

# Flask-Session 설정
app.config["SESSION_TYPE"] = "filesystem"  # 세션을 파일 시스템에 저장
Session(app)

if __name__ == "__main__":
    print(app.url_map)  # URL 매핑 출력
    app.run(host="0.0.0.0", port=5005, debug=True)

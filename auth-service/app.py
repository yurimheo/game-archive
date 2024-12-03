import os
from app import create_app
from app.views import auth_blueprint  # views.py를 import
from flask_session import Session
from app.models import init_db
import redis

# Flask 앱 생성
app = create_app()

# 블루프린트 등록
app.register_blueprint(auth_blueprint)

# Secret Key 설정
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")

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

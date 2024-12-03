import os
from app import create_app
from app.views import main_blueprint
from flask_session import Session
import redis

# Flask 앱 생성
app = create_app()


# 블루프린트 등록
app.register_blueprint(main_blueprint)

# Secret Key 설정
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")

# Flask-Session 설정
app.config["SESSION_TYPE"] = "redis"  # 세션을 Redis로 설정
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_REDIS"] = redis.StrictRedis(host='redis', port=6379, db=0)

Session(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

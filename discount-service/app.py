import os
from app import create_app
from app.views import discounts_blueprint  # views.py에서 블루프린트 가져오기
from flask_session import Session
import redis

# Flask 앱 생성
app = create_app()

# 블루프린트 등록
app.register_blueprint(discounts_blueprint, url_prefix='/discounts')

# Secret Key 설정
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")

# Flask-Session 설정
app.config["SESSION_TYPE"] = "redis"  # 세션을 Redis로 설정
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_REDIS"] = redis.StrictRedis(host='redis', port=6379, db=0)

Session(app)

if __name__ == "__main__":
    print(app.url_map)  # URL 매핑 출력
    app.run(host="0.0.0.0", port=5002, debug=True)

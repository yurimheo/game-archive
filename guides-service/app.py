from flask import Flask
from app.views import guide_blueprint  # views.py에서 Blueprint 가져오기
from flask_session import Session
import redis
import os
from app.models import db_session
from app.auth_proxy import auth_proxy

# Flask 앱 생성
app = Flask(__name__,
            static_folder='app/static',
            template_folder='app/templates')

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "supersecretkey")
app.config["SESSION_TYPE"] = "redis"  # 세션을 Redis로 설정
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_REDIS"] = redis.StrictRedis(host='redis', port=6379, db=0)

# 블루프린트 등록
app.register_blueprint(guide_blueprint, url_prefix='/guide')
app.register_blueprint(auth_proxy, url_prefix='/auth')  # /auth 경로에 auth_proxy 블루프린트 등록

# Flask-Session 설정
Session(app)


@app.teardown_appcontext
def remove_db_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)

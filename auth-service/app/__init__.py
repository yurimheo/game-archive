# 플라스크 초기화 코드 (인증 서비스)
from flask import Flask

def create_app():
    app = Flask(__name__)

    # Blueprint 등록
    from .routes import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app

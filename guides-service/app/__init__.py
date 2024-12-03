from flask import Flask
from app.config import Config  # Config 설정을 가져옵니다

def create_app():
    app = Flask(__name__,
                static_folder='app/static',
                template_folder='app/templates')

    # 설정 적용
    app.config.from_object(Config)

    from app.views import guide_blueprint
    app.register_blueprint(guide_blueprint)

    return app

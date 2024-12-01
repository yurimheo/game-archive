from flask import Flask

def create_app():
    app = Flask(__name__)

    # 블루프린트 등록
    from .views import timedeal_blueprint
    app.register_blueprint(timedeal_blueprint, url_prefix='/timedeal')

    return app

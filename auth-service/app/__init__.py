import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()  # 전역으로 SQLAlchemy 인스턴스를 생성합니다.


def create_app():
    app = Flask(__name__)

    # 데이터베이스 설정
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URI', 'mysql+pymysql://admin:admin@localhost/game_archive'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'supersecretkey')

    # SQLAlchemy 초기화
    db.init_app(app)

    # Flask-Migrate 초기화
    Migrate(app, db)

    # 블루프린트 등록
    from app.views import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
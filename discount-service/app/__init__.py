import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # 앱 설정
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI", "mysql+pymysql://admin:admin@localhost/game_archive")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "default_secret_key")
    
    # DB 초기화
    db.init_app(app)

    return app

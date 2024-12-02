from flask import Flask
from sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # SQLAlchemy 객체 생성

def create_app():
    app = Flask(__name__)
    
    # 데이터베이스 설정
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # SQLAlchemy와 Flask 애플리케이션 연결
    db.init_app(app)
    
    # Migrate와 Flask 애플리케이션 및 데이터베이스 연결
    migrate.init_app(app, db)

    return app

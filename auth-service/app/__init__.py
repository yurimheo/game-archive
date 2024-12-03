from flask import Flask
from sqlalchemy.orm import scoped_session
from app.models import Base, SessionLocal, engine

def create_app():
    app = Flask(__name__)

    # Flask 설정
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://admin:admin@mysql:3306/game_archive"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # SQLAlchemy에서 불필요한 추적을 비활성화
    app.config['SECRET_KEY'] = "supersecretkey"

    # SQLAlchemy 세션 설정
    app.session = scoped_session(SessionLocal)

    # 데이터베이스 초기화
    with app.app_context():
        Base.metadata.create_all(bind=engine)  # 테이블 생성

    return app

from flask import Flask, session, request
from flask_session import Session
from flask_jwt_extended import JWTManager
from app.views import auth_blueprint

def create_app():
    app = Flask(__name__)
    
    # 기존 설정 유지
    app.config['SECRET_KEY'] = 'your-secret-key'  # 비밀 키
    app.config['SESSION_TYPE'] = 'filesystem'     # 세션 타입

    # JWT 설정 추가
    app.config['JWT_SECRET_KEY'] = 'your-jwt-secret-key'  # JWT 비밀 키
    jwt = JWTManager(app)  # JWT 매니저 초기화

    # 세션 초기화
    Session(app)

    # 블루프린트 등록
    app.register_blueprint(auth_blueprint, url_prefix='/')  # URL 접두사 추가로 명시적으로 등록

    return app

from flask import Flask, session, request, g
from flask_session import Session
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_identity
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

    # JWT를 사용한 로그인 상태 확인
    @app.before_request
    def load_logged_in_user():
        g.user = None  # 기본값으로 로그인되지 않은 상태로 설정
        try:
            # JWT 검증 및 사용자 ID 추출
            verify_jwt_in_request(optional=True)
            current_user = get_jwt_identity()
            if current_user:
                g.user = {"username": current_user}  # 사용자 정보 저장
        except Exception as e:
            # JWT가 없거나 유효하지 않으면 g.user를 None으로 유지
            pass

    # 블루프린트 등록
    app.register_blueprint(auth_blueprint, url_prefix='/')  # URL 접두사 추가로 명시적으로 등록

    return app

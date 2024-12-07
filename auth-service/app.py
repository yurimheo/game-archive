import os
from app import create_app
from app.views import auth_blueprint  # views.py를 import
from app.models import init_db
from flask import Flask, g, request, jsonify
import jwt as pyjwt
import redis

# Flask 앱 생성
app = create_app()

# 블루프린트 등록
app.register_blueprint(auth_blueprint)

# Secret Key 설정
SECRET_KEY = "supersecretkey"

@app.before_request
def load_logged_in_user():
    """
    요청 전에 JWT를 확인하고 사용자 정보를 g.user에 저장합니다.
    """
    token = request.cookies.get('access_token')  # 클라이언트에서 보낸 토큰
    g.user = None

    if token:
        try:
            # JWT 디코딩
            decoded_token = pyjwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            g.user = {
                "user_id": decoded_token.get("user_id"),
                "username": decoded_token.get("username"),
            }
        except pyjwt.ExpiredSignatureError:
            pass  # 토큰 만료시 g.user를 None으로 둠
        except pyjwt.InvalidTokenError:
            pass  # 유효하지 않은 토큰

@app.context_processor
def inject_user():
    """
    템플릿에 g.user를 user 변수로 전달합니다.
    """
    return {"user": g.user}

@app.route('/api/users/batch', methods=['POST'])
def get_user_info():
    user_ids = request.json.get("user_ids", [])
    # 데이터베이스에서 사용자 정보 조회 (예시 데이터 반환)
    users = {
        1: {"username": "player1"},
        2: {"username": "gamer2"},
        # 더 많은 사용자 추가
    }
    return jsonify({uid: users.get(uid, {"username": "알 수 없는 사용자"}) for uid in user_ids})

# 데이터베이스 초기화
init_db()

if __name__ == "__main__":
    print(app.url_map)  # URL 매핑 출력
    app.run(host="0.0.0.0", port=5006, debug=True)


@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    단일 사용자 정보를 반환하는 엔드포인트
    """
    # 사용자 데이터베이스 시뮬레이션
    users = {
        1: {"username": "Alice"},
        21: {"username": "test"},
        42: {"username": "Bob"}
    }

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    단일 사용자 정보를 반환하는 엔드포인트
    """
    # 임시 사용자 데이터베이스
    users = {
        1: {"username": "Alice"},
        21: {"username": "test"},
        42: {"username": "Bob"}
    }

    # 사용자 조회
    user = users.get(user_id)
    if user:
        return jsonify({"user_id": user_id, "username": user["username"]}), 200
    return jsonify({"error": "User not found"}), 404


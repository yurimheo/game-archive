from flask import Blueprint, jsonify, request, make_response, render_template, redirect, url_for
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

# 블루프린트 생성
auth_blueprint = Blueprint(
    'auth',
    __name__,
    template_folder='templates',
    static_folder='static'
)

# JWT 토큰 만료 시간 설정
TOKEN_EXPIRES_IN_HOURS = 1

# 로그인 처리
@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "test" and password == "password":
            access_token = create_access_token(identity=username, expires_delta=timedelta(hours=1))
            response = make_response(redirect("http://127.0.0.1:5001"))
            response.set_cookie("access_token", access_token, httponly=True)
            return response

        return jsonify({"message": "로그인 실패"}), 401

    # GET 요청: 로그인 페이지 렌더링
    return render_template("login.html")

# 로그아웃 처리
@auth_blueprint.route('/logout', methods=['POST'])
def logout():
    response = make_response(jsonify({"message": "로그아웃 성공"}))
    response.delete_cookie("access_token")  # 쿠키에서 JWT 삭제
    return response

# 로그인 상태 확인 API
@auth_blueprint.route('/check-login', methods=['GET'])
@jwt_required(optional=True)  # JWT가 없어도 호출 가능
def check_login():
    current_user = get_jwt_identity()
    if current_user:
        return jsonify({"logged_in": True, "username": current_user}), 200
    return jsonify({"logged_in": False}), 200

# 회원가입 처리
@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        email = request.form.get('email')

        if len(username) < 3:
            return jsonify({"success": False, "error": "아이디는 최소 3자 이상이어야 합니다."}), 400
        if password != confirm_password:
            return jsonify({"success": False, "error": "비밀번호가 일치하지 않습니다."}), 400

        return jsonify({"success": True}), 200

    # GET 요청: 회원가입 페이지 렌더링
    return render_template("register.html")

# 마이페이지
@auth_blueprint.route('/mypage', methods=['GET'])
@jwt_required()
def mypage():
    current_user = get_jwt_identity()
    return render_template('mypage.html', user={'username': current_user})

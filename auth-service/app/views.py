from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

# 블루프린트 생성
auth_blueprint = Blueprint(
    'auth',
    __name__,
    template_folder='templates',
    static_folder='static'
)

# 로그인 처리
@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 폼 데이터 가져오기
        username = request.form.get('username')
        password = request.form.get('password')
        # 임시 사용자 인증 로직
        if username == 'test' and password == 'password':
            # JWT 생성
            access_token = create_access_token(identity=username, expires_delta=timedelta(hours=1))
            response = make_response(redirect("http://127.0.0.1:5001"))
            response.set_cookie('access_token', access_token, httponly=True)
            flash('로그인 성공!', 'success')
            return response
        flash('로그인 실패!', 'danger')
    # 로그인 페이지 렌더링
    return render_template('login.html')

# 회원가입 처리
@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 폼 데이터 가져오기
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        email = request.form.get('email')

        # 유효성 검사
        if len(username) < 3:
            # 아이디가 3자 미만인 경우 오류 메시지 반환
            return render_template('register.html', error_username="아이디는 최소 3자 이상이어야 합니다.")
        if password != confirm_password:
            # 비밀번호가 일치하지 않는 경우 오류 메시지 반환
            return render_template('register.html', error_password="비밀번호가 일치하지 않습니다.")

        # 회원가입 성공 처리
        flash(f"'{username}' 계정이 성공적으로 생성되었습니다!", 'success')
        # 로그인 페이지로 리디렉션
        return redirect(url_for('auth.login'))

    # 회원가입 페이지 렌더링
    return render_template('register.html')

# 마이페이지
@auth_blueprint.route('/mypage', methods=['GET'])
@jwt_required()
def mypage():
    current_user = get_jwt_identity()
    return render_template('mypage.html', user={'username': current_user})

# 로그아웃 라우트
@auth_blueprint.route('/logout', methods=['POST'])  # POST 메서드 사용
def logout():
    response = make_response(redirect(url_for('auth.login')))
    response.delete_cookie('access_token')  # 쿠키에서 JWT 삭제
    flash('로그아웃 되었습니다.', 'info')  # 로그아웃 알림 메시지
    return response

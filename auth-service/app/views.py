from flask import Blueprint, render_template, request, redirect, url_for, flash

# 블루프린트 생성
auth_blueprint = Blueprint(
    'auth',
    __name__,
    template_folder='app/templates',
    static_folder='app/static'
)

# 로그인 페이지
@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 로그인 로직 (예: 사용자 인증)
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'test' and password == 'password':  # 예제 사용자
            flash('로그인 성공!', 'success')
            return redirect(url_for('auth.mypage'))
        flash('로그인 실패!', 'danger')
    return render_template('login.html')

# 회원가입 페이지
@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 폼 데이터 가져오기
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        email = request.form.get('email')

        # 유효성 검사
        error_username = None
        error_password = None
        if len(username) < 3:
            error_username = "아이디는 최소 3자 이상이어야 합니다."
        if password != confirm_password:
            error_password = "비밀번호가 일치하지 않습니다."

        # 에러가 있는 경우 템플릿에 에러 메시지 전달
        if error_username or error_password:
            return render_template(
                'register.html',
                error_username=error_username,
                error_password=error_password
            )

        # 회원가입 성공 처리 (DB 저장 등은 나중에 추가)
        flash(f"'{username}' 계정이 성공적으로 생성되었습니다!", 'success')
        return redirect(url_for('auth.login'))

    # GET 요청일 경우 회원가입 페이지 렌더링
    return render_template('register.html')
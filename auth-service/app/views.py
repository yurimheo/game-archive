from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import SessionLocal, User
from werkzeug.security import generate_password_hash, check_password_hash

auth_blueprint = Blueprint(
    'auth',
    __name__,
    template_folder='app/templates',
    static_folder='app/static'
)

# 회원가입
@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 폼 데이터 가져오기
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # 유효성 검사
        if len(username) < 3:
            flash("아이디는 최소 3자 이상이어야 합니다.", "danger")
            return render_template('register.html')
        if '@' not in email:
            flash("유효한 이메일 주소를 입력하세요.", "danger")
            return render_template('register.html')
        if password != confirm_password:
            flash("비밀번호가 일치하지 않습니다.", "danger")
            return render_template('register.html')

        # 데이터베이스 연결 및 사용자 저장
        session_db = SessionLocal()
        existing_user = session_db.query(User).filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash("이미 존재하는 사용자입니다.", "danger")
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, email=email, password=hashed_password)
            session_db.add(new_user)
            session_db.commit()
            flash("회원가입이 성공적으로 완료되었습니다.", "success")
            session_db.close()
            return redirect(url_for('auth.login'))

        session_db.close()

    return render_template('register.html')

# 로그인
@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # 데이터베이스에서 사용자 정보 확인
        session_db = SessionLocal()
        user = session_db.query(User).filter(User.username == username).first()
        session_db.close()

        if user and check_password_hash(user.password, password):
            # 로그인 성공
            session['user_id'] = user.user_id
            session['username'] = user.username
            flash(f"'{user.username}'님, 환영합니다!", "success")
            return redirect(url_for('auth.mypage'))
        else:
            flash("아이디 또는 비밀번호가 잘못되었습니다.", "danger")

    return render_template('login.html')

# 마이페이지
@auth_blueprint.route('/mypage')
def mypage():
    if 'user_id' not in session:
        flash("로그인이 필요합니다.", "danger")
        return redirect(url_for('auth.login'))

    # 데이터베이스에서 사용자 정보 조회
    session_db = SessionLocal()
    user = session_db.query(User).filter(User.user_id == session['user_id']).first()
    session_db.close()

    if not user:
        flash("사용자 정보를 찾을 수 없습니다.", "danger")
        return redirect(url_for('auth.login'))

    return render_template('mypage.html', user=user)


# 로그아웃
@auth_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    flash('성공적으로 로그아웃되었습니다.', 'success')
    return redirect(url_for('auth.login'))

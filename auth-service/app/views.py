from flask import Blueprint, jsonify, make_response, render_template, request, redirect, url_for, flash, session
from app.models import SessionLocal, User
from werkzeug.security import generate_password_hash, check_password_hash
import jwt as pyjwt
import datetime

SECRET_KEY = "supersecretkey"
REFRESH_SECRET_KEY = "superrefreshsecretkey"

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
            # Access Token 발급
            access_token = pyjwt.encode(
                {
                    "user_id": user.user_id,
                    "username": user.username,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
                },
                SECRET_KEY,
                algorithm="HS256"
            )

            # Refresh Token 발급
            refresh_token = pyjwt.encode(
                {
                    "user_id": user.user_id,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)
                },
                REFRESH_SECRET_KEY,
                algorithm="HS256"
            )

            # 응답에 쿠키 설정
            response = redirect(url_for('auth.mypage'))  # 로그인 성공 후 이동할 페이지
            response.set_cookie(
                "access_token",
                access_token,
                httponly=True,  # JavaScript에서 접근하지 못하도록 설정
                secure=False,  # HTTPS 환경에서는 True로 설정
                samesite="Lax"
            )
            response.set_cookie(
                "refresh_token",
                refresh_token,
                httponly=True,
                secure=False,
                samesite="Lax",
                domain="127.0.0.1"
            )
            return response

        flash("아이디 또는 비밀번호가 잘못되었습니다.", "danger")

    return render_template('login.html')

# 마이페이지
@auth_blueprint.route('/mypage')
def mypage():
    """
    마이페이지 - Access Token을 확인하고 필요 시 Refresh Token으로 갱신합니다.
    """
    # 쿠키에서 Access Token과 Refresh Token 가져오기
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")

    if not access_token:
        flash("로그인이 필요합니다.", "danger")
        return redirect(url_for('auth.login'))

    try:
        # Access Token 검증
        decoded = pyjwt.decode(access_token, SECRET_KEY, algorithms=["HS256"])
        user_id = decoded["user_id"]

    except pyjwt.ExpiredSignatureError:
        # Access Token 만료 시 Refresh Token 사용
        if not refresh_token:
            flash("세션이 만료되었습니다. 다시 로그인해주세요.", "danger")
            return redirect(url_for('auth.login'))

        try:
            # Refresh Token 검증 및 새로운 Access Token 발급
            decoded_refresh = pyjwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=["HS256"])
            user_id = decoded_refresh["user_id"]

            new_access_token = pyjwt.encode(
                {"user_id": user_id, "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)},
                SECRET_KEY,
                algorithm="HS256"
            )

            # 새 Access Token 쿠키 설정
            response = make_response(redirect(url_for('auth.mypage')))
            response.set_cookie(
                "access_token",
                new_access_token,
                httponly=True,
                secure=False,
                samesite="Lax",
                domain="127.0.0.1"
            )
            return response

        except pyjwt.ExpiredSignatureError:
            flash("세션이 만료되었습니다. 다시 로그인해주세요.", "danger")
            return redirect(url_for('auth.login'))
        except pyjwt.InvalidTokenError:
            flash("유효하지 않은 인증 정보입니다.", "danger")
            return redirect(url_for('auth.login'))

    except pyjwt.InvalidTokenError:
        flash("유효하지 않은 인증 정보입니다.", "danger")
        return redirect(url_for('auth.login'))

    # 데이터베이스에서 사용자 정보 조회
    session_db = SessionLocal()
    user = session_db.query(User).filter(User.user_id == user_id).first()
    session_db.close()

    if not user:
        flash("사용자 정보를 찾을 수 없습니다.", "danger")
        return redirect(url_for('auth.login'))

    # 사용자 정보를 마이페이지 템플릿으로 전달
    return render_template('mypage.html', user=user)


# 로그아웃
@auth_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    """
    로그아웃 시 Access Token 및 Refresh Token 쿠키를 삭제합니다.
    """
    response = redirect(url_for('auth.login'))
    response.set_cookie('access_token', '', expires=0)  # Access Token 삭제
    response.set_cookie('refresh_token', '', expires=0)  # Refresh Token 삭제
    flash('성공적으로 로그아웃되었습니다.', 'success')
    return response

# Refresh 토큰
@auth_blueprint.route("/refresh", methods=["POST"])
def refresh_token():
    """
    Refresh Token을 사용하여 새로운 Access Token을 발급합니다.
    """
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        return jsonify({"error": "Refresh token is missing"}), 400

    try:
        # Refresh Token 검증
        decoded = pyjwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=["HS256"])
        user_id = decoded["user_id"]

        # 새로운 Access Token 발급
        new_access_token = pyjwt.encode(
            {"user_id": user_id, "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)},
            SECRET_KEY,
            algorithm="HS256"
        )

        # Access Token 쿠키 갱신
        response = jsonify({"access_token": new_access_token})
        response.set_cookie(
            "access_token",
            new_access_token,
            httponly=True,
            secure=False,
            samesite="Lax"
        )
        return response, 200

    except pyjwt.ExpiredSignatureError:
        return jsonify({"error": "Refresh token expired"}), 401
    except pyjwt.InvalidTokenError:
        return jsonify({"error": "Invalid refresh token"}), 401

@auth_blueprint.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(user_id=user_id).first()
        if user:
            return jsonify({"user_id": user.user_id, "username": user.username}), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()
import requests
from flask import Blueprint, redirect, url_for, flash, session

auth_proxy = Blueprint('auth', __name__)

AUTH_SERVICE_URL = "http://127.0.0.1:5006"

@auth_proxy.route('/login/callback')
def login_callback():
    """auth-service에서 인증 후 리디렉션된 콜백 처리"""
    token = request.args.get('token')  # auth-service에서 반환한 인증 토큰
    if not token:
        flash("인증 토큰이 누락되었습니다.", "danger")
        return redirect(f"{AUTH_SERVICE_URL}/login")

    try:
        # auth-service에 토큰 확인 요청
        response = requests.get(f"{AUTH_SERVICE_URL}/verify", params={"token": token}, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        flash("인증 서버와 통신 중 문제가 발생했습니다.", "danger")
        return redirect(f"{AUTH_SERVICE_URL}/login")

    if response.status_code == 200:
        # 인증 성공 - 사용자 정보를 세션에 저장
        user_data = response.json()
        session['user_id'] = user_data['user_id']
        session['username'] = user_data['username']
        flash("로그인 성공!", "success")
        return redirect(url_for('guide.guide_list'))
    else:
        flash("인증 실패. 다시 로그인하세요.", "danger")
        return redirect(f"{AUTH_SERVICE_URL}/login")

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, g
from datetime import datetime, timedelta
import random
import string
import logging
import jwt as pyjwt

# 블루프린트 정의
timedeal_blueprint = Blueprint(
    'timedeal',
    __name__,
    template_folder='templates',
    static_folder='static'
)

SECRET_KEY = "supersecretkey"

# 쿠폰 데이터
coupons = {
    "remaining": 10,
    "reset_time": None,
    "generated_coupons": []
}

def reset_coupons():
    """쿠폰 리셋"""
    coupons["remaining"] = 10
    coupons["reset_time"] = datetime.now() + timedelta(hours=1)
    coupons["generated_coupons"] = []

from functools import wraps

def login_required(func):
    """로그인 여부 확인 데코레이터"""
    @wraps(func)  # 원래 함수의 이름과 속성을 유지
    def wrapper(*args, **kwargs):
        token = request.cookies.get("access_token")
        if not token:
            return redirect("http://127.0.0.1:5006/login")
        try:
            decoded_token = pyjwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            g.user = {
                "user_id": decoded_token.get("user_id"),
                "username": decoded_token.get("username")
            }
        except pyjwt.ExpiredSignatureError:
            logging.info("Access token expired")
            return redirect("http://127.0.0.1:5006/login")
        except pyjwt.InvalidTokenError:
            logging.info("Invalid token")
            return redirect("http://127.0.0.1:5006/login")

        return func(*args, **kwargs)
    return wrapper

# 타임딜 페이지
@timedeal_blueprint.route('/')
@login_required
def timedeal():
    now = datetime.now()

    # 리셋 시간 체크
    if not coupons["reset_time"] or now >= coupons["reset_time"]:
        reset_coupons()

    return render_template(
        'timedeal.html',
        remaining_coupons=coupons["remaining"],
        reset_time=coupons["reset_time"].strftime("%Y-%m-%d %H:%M:%S"),
        user=g.user
    )

# 쿠폰 생성 API
@timedeal_blueprint.route('/coupon', methods=['POST'])
@login_required
def generate_coupon():
    if coupons["remaining"] <= 0:
        return jsonify({"error": "더 이상 쿠폰을 발급할 수 없습니다!"}), 400

    # 랜덤 쿠폰 생성
    coupon = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
    coupons["generated_coupons"].append(coupon)
    coupons["remaining"] -= 1

    logging.info(f"쿠폰 발급: {coupon}")
    return jsonify({"coupon": coupon})

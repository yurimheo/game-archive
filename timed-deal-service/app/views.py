from flask import Blueprint, render_template, request, jsonify
from datetime import datetime, timedelta
import random
import string
import logging

# 블루프린트 정의
timedeal_blueprint = Blueprint(
    'timedeal',
    __name__,
    template_folder='templates',
    static_folder='static'
)

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

# 타임딜 페이지
@timedeal_blueprint.route('/')
def timedeal():
    now = datetime.now()

    # 리셋 시간 체크
    if not coupons["reset_time"] or now >= coupons["reset_time"]:
        reset_coupons()

    return render_template(
        'timedeal.html',
        remaining_coupons=coupons["remaining"],
        reset_time=coupons["reset_time"].strftime("%Y-%m-%d %H:%M:%S")
    )

# 쿠폰 생성 API
@timedeal_blueprint.route('/coupon', methods=['POST'])
def generate_coupon():
    if coupons["remaining"] <= 0:
        return jsonify({"error": "더 이상 쿠폰을 발급할 수 없습니다!"}), 400

    # 랜덤 쿠폰 생성
    coupon = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
    coupons["generated_coupons"].append(coupon)
    coupons["remaining"] -= 1

    logging.info(f"쿠폰 발급: {coupon}")
    return jsonify({"coupon": coupon})

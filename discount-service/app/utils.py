import jwt as pyjwt
from flask import request, jsonify
from functools import wraps
import requests
import logging
import threading
import time
from datetime import datetime, timedelta

SECRET_KEY = "supersecretkey"

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print("Decoded token:", g.user)
        
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization token required"}), 401

        token = auth_header.split(" ")[1]
        try:
            decoded_token = pyjwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user = decoded_token  
        except pyjwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except pyjwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated_function

# 전역 변수
cached_games = []
cache_expiry = 0
cache_lock = threading.Lock()

# Steam API에서 데이터 가져오기
def get_games():
    global cached_games, cache_expiry
    with cache_lock:
        current_time = time.time()
        if current_time < cache_expiry:
            logging.info("캐시된 게임 데이터를 사용합니다.")
            return cached_games

        url = "https://store.steampowered.com/api/featuredcategories"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            logging.error(f"API 호출 에러: {e}")
            return cached_games  # 이전 캐시 데이터를 반환하거나 빈 리스트 반환

        data = response.json()
        categories = ['specials', 'coming_soon', 'top_sellers', 'new_releases']
        games = []
        seen_game_ids = set()  # 중복 방지를 위한 집합

        for category in categories:
            items = data.get(category, {}).get("items", [])
            logging.info(f"카테고리 '{category}'의 게임 수: {len(items)}")
            for game in items:
                game_id = game.get("id")
                if not game_id:
                    continue  # ID가 없는 게임은 건너뜀
                if game_id in seen_game_ids:
                    continue  # 이미 추가된 게임은 건너뜀
                seen_game_ids.add(game_id)

                # 필수 필드 존재 여부 확인
                name = game.get("name", "Unknown")
                discount_percent = game.get("discount_percent", 0)
                original_price = game.get("original_price")
                final_price = game.get("final_price")
                image_url = game.get("large_capsule_image", "")
                category_name = category.replace('_', ' ').title()  # 카테고리 이름 추가

                # 가격 정보가 없는 경우 처리
                if original_price is None or final_price is None:
                    original_price_display = "무료"  # 또는 다른 기본값
                    final_price_display = "무료"
                else:
                    original_price_display = f"{int(original_price / 100):,}".replace(",", ".")  # 예: "1.500.000"
                    final_price_display = f"{int(final_price / 100):,}".replace(",", ".")  # 예: "1.350.000" 이런식으로 단위 체크 가능하도록 설정

                games.append({
                    "id": game_id,
                    "name": name,
                    "discount_percent": discount_percent,
                    "original_price": original_price_display,
                    "final_price": final_price_display,
                    "image_url": image_url,
                    "category": category_name  # 카테고리 이름 추가
                })

        # 캐시 갱신 (예: 1시간 후 만료)
        cached_games = games
        cache_expiry = current_time + 3600  # 1시간
        logging.info(f"캐시된 게임 수: {len(games)}")
        return games
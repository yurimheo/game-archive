import logging
import threading
import time
import requests
from flask import Blueprint, render_template, g, request, jsonify
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import jwt as pyjwt

SECRET_KEY = "supersecretkey"
DATABASE_URI = "mysql+pymysql://admin:admin@mysql:3306/game_archive"

# 블루프린트 생성
main_blueprint = Blueprint('main', __name__)

# SQLAlchemy 세션 설정
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 캐싱을 위한 전역 변수
cached_games = []
cache_expiry = 0
cache_lock = threading.Lock()

def get_games():
    """Steam API에서 할인 게임 데이터를 가져오고 캐싱"""
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
            return cached_games

        data = response.json()
        categories = ['specials', 'coming_soon', 'top_sellers', 'new_releases']
        games = []
        seen_game_ids = set()

        for category in categories:
            items = data.get(category, {}).get("items", [])
            for game in items:
                game_id = game.get("id")
                if not game_id or game_id in seen_game_ids:
                    continue
                seen_game_ids.add(game_id)

                games.append({
                    "id": game_id,
                    "name": game.get("name", "Unknown"),
                    "discount_percent": game.get("discount_percent", 0),
                    "original_price": game.get("original_price", "무료"),
                    "final_price": game.get("final_price", "무료"),
                    "image_url": game.get("large_capsule_image", ""),
                    "category": category.replace('_', ' ').title()
                })

        cached_games = games
        cache_expiry = current_time + 3600
        logging.info(f"캐시된 게임 수: {len(games)}")
        return games

# JWT 검증 로직
@main_blueprint.before_app_request
def load_logged_in_user():
    token = request.cookies.get("access_token")
    g.user = None

    if token:
        try:
            decoded_token = pyjwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            g.user = {
                "user_id": decoded_token.get("user_id"),
                "username": decoded_token.get("username"),
            }
        except pyjwt.ExpiredSignatureError:
            logging.info("Access token expired")
        except pyjwt.InvalidTokenError:
            logging.info("Invalid token")

# 메인 페이지 라우트
@main_blueprint.route('/')
def main_page():
    games = get_games()
    highlighted_games = games[:12]
    return render_template('main.html', highlighted_games=highlighted_games, user=g.user)
import requests
import logging
import threading
import time
from datetime import datetime, timedelta

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
            data = response.json()
        except requests.RequestException as e:
            logging.error(f"API 호출 실패: {e}")
            return cached_games

        games = process_games(data)
        cached_games = games
        cache_expiry = current_time + 3600  # 1시간 캐시
        return games

def process_games(data):
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
    return games

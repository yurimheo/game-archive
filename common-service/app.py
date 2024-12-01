import logging
import threading
import time
import requests
from flask import Flask, render_template

# Flask 앱 생성
app = Flask(__name__,
            static_folder='static',
            template_folder='templates')

# 로깅 설정
logging.basicConfig(level=logging.INFO)

# 캐싱을 위한 전역 변수
cached_games = []
cache_expiry = 0
cache_lock = threading.Lock()

# Steam 게임 데이터 가져오기
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
                if not game_id or game_id in seen_game_ids:
                    continue  # ID가 없거나 이미 추가된 게임은 건너뜀
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
                    original_price_display = f"{original_price:,} 원".replace(",", ".")  
                    final_price_display = f"{final_price:,} 원".replace(",", ".") 

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

# 메인 페이지 라우트
@app.route('/')
def main_page():
    """메인 페이지"""
    # 할인 게임 데이터 가져오기
    games = get_games()

    # 최대 12개 게임만 메인 페이지에 표시
    highlighted_games = games[:12]

    return render_template(
        'main.html',
        highlighted_games=highlighted_games  # 템플릿으로 데이터 전달
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

from flask import Blueprint, render_template, request, g
from app.utils import get_games

# 블루프린트 생성
discounts_blueprint = Blueprint('discounts', __name__, url_prefix='/discounts')

# 할인 목록 페이지
@discounts_blueprint.route('/')
def index():
    # Steam 게임 리스트 가져오기
    games = get_games()

    # 필터 처리
    filter_type = request.args.get('filter', 'high')
    category_filter = request.args.get('category')  # 카테고리 필터 추가

    if filter_type == 'high':
        games = sorted(games, key=lambda x: x['discount_percent'], reverse=True)
    elif filter_type == 'low':
        games = sorted(games, key=lambda x: x['discount_percent'])

    if category_filter:
        games = [game for game in games if game['category'] == category_filter]

    # 페이지네이션 처리
    try:
        page = int(request.args.get('page', 1))
        if page < 1:
            page = 1
    except ValueError:
        page = 1

    per_page = 12
    start = (page - 1) * per_page
    end = start + per_page
    paginated_games = games[start:end]
    total_pages = (len(games) + per_page - 1) // per_page

    # discounts.html 템플릿 렌더링
    return render_template(
        'discounts.html',
        games=paginated_games,
        filter_type=filter_type,
        category_filter=category_filter,
        current_page=page,
        total_pages=total_pages,
        user=g.user  # 로그인된 사용자 정보 전달
    )
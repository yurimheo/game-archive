from flask import Blueprint, render_template, request

# 블루프린트 생성
news_blueprint = Blueprint(
    'news', 
    __name__, 
    template_folder='app/templates', 
    static_folder='app/static'
)

# /news 라우팅 - 뉴스 목록
@news_blueprint.route('/news')
def news():
    # 더미 데이터로 뉴스 목록 생성
    all_news = [
        {'id': 1, 'title': '게임 뉴스 더미 테스트 1', 'date': '2024. 11. 26.', 'image_url': 'https://via.placeholder.com/300x200'},
        {'id': 2, 'title': '게임 뉴스 더미 테스트 2', 'date': '2024. 11. 26.', 'image_url': 'https://via.placeholder.com/300x200'},
        {'id': 3, 'title': '게임 뉴스 더미 테스트 3', 'date': '2024. 11. 25.', 'image_url': 'https://via.placeholder.com/300x200'},
        {'id': 4, 'title': '게임 뉴스 더미 테스트 4', 'date': '2024. 11. 25.', 'image_url': 'https://via.placeholder.com/300x200'},
        {'id': 5, 'title': '게임 뉴스 더미 테스트 5', 'date': '2024. 11. 24.', 'image_url': 'https://via.placeholder.com/300x200'},
        {'id': 6, 'title': '게임 뉴스 더미 테스트 6', 'date': '2024. 11. 24.', 'image_url': 'https://via.placeholder.com/300x200'},
        {'id': 7, 'title': '게임 뉴스 더미 테스트 7', 'date': '2024. 11. 23.', 'image_url': 'https://via.placeholder.com/300x200'},
        {'id': 8, 'title': '게임 뉴스 더미 테스트 8', 'date': '2024. 11. 23.', 'image_url': 'https://via.placeholder.com/300x200'},
        # 추가 데이터...
    ]

    # 페이지네이션 처리
    per_page = 6  # 페이지당 항목 수
    total_pages = (len(all_news) + per_page - 1) // per_page  # 전체 페이지 수 계산

    # 현재 페이지 번호 가져오기
    current_page = int(request.args.get('page', 1))  # 기본값: 1
    if current_page < 1 or current_page > total_pages:
        current_page = 1  # 잘못된 페이지 번호 처리

    # 현재 페이지에 해당하는 데이터 슬라이싱
    start_index = (current_page - 1) * per_page
    end_index = start_index + per_page
    news_list = all_news[start_index:end_index]

    return render_template(
        'news.html',
        news_list=news_list,
        current_page=current_page,
        total_pages=total_pages
    )



# /news/<int:news_id> 라우팅 - 뉴스 상세
# views.py
@news_blueprint.route('/news/<int:news_id>')
def news_detail(news_id):
    news = {
        'id': news_id,
        'title': f'게임 뉴스 더미 테스트 {news_id}',
        'content': '뉴스 내용이 여기에 들어갑니다. 이 부분은 여러 단락으로 구성될 수 있습니다.',
        'comments': [
            {'author': 'User1', 'text': '댓글 내용 1'},
            {'author': 'User2', 'text': '댓글 내용 2'},
        ]
    }
    return render_template('news_detail.html', news=news)


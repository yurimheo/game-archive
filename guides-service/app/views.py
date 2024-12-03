import logging
import threading
import time
import redis
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from app.models import db_session, Guide, GameCategory
from app.utils import login_required 

# Redis 연결 설정
redis_client = redis.StrictRedis(host='redis', port=6379, decode_responses=True)

# SQLAlchemy 세션 설정
DATABASE_URI = "mysql+pymysql://admin:admin@mysql:3306/game_archive"
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 블루프린트 생성
guide_blueprint = Blueprint('guide', __name__)

# 캐싱을 위한 전역 변수
cached_guides = []
cache_expiry = 0
cache_lock = threading.Lock()

def get_guides():
    """공략 데이터를 가져오고 캐싱"""
    global cached_guides, cache_expiry
    with cache_lock:
        current_time = time.time()
        if current_time < cache_expiry:
            logging.info("캐시된 공략 데이터를 사용합니다.")
            return cached_guides

        # SQLAlchemy 세션 사용
        db_session = SessionLocal()
        guides = db_session.query(Guide).all()
        cached_guides = guides
        cache_expiry = current_time + 3600  # 1시간 캐시
        logging.info(f"캐시된 공략 수: {len(guides)}")
        db_session.close()
        return guides

def get_user_info(user_id):
    """Redis에서 사용자 정보를 가져옵니다"""
    if not user_id:
        return None

    # Redis에서 사용자 이름 가져오기
    username = redis_client.get(f"user:{user_id}:username")
    if not username:
        logging.warning(f"Redis에서 사용자 {user_id} 정보를 찾을 수 없습니다.")
        return None

    return username

@guide_blueprint.route('/')
def guide_list():
    page = request.args.get('page', 1, type=int)
    per_page = 10

    # 공략 목록 가져오기 (최신순)
    guides_query = db_session.query(Guide).order_by(desc(Guide.created_at))
    total_items = guides_query.count()
    total_pages = (total_items + per_page - 1) // per_page
    guides = guides_query.offset((page - 1) * per_page).limit(per_page).all()
# 모든 사용자 데이터 가져오기 (캐싱 가능)
    users = {user.user_id: user.username for user in db_session.query(User).all()}

    # 각 공략에 글쓴이 이름 추가
    for guide in guides:
        guide.author_name = users.get(guide.user_id, "알 수 없음")

    # 인기 공략 조회
    popular_guides = db_session.query(Guide).order_by(desc(Guide.views)).limit(5).all()
    for guide in popular_guides:
        guide.author_name = users.get(guide.user_id, "알 수 없음")

    return render_template(
        'guide_list.html',
        guides=guides,
        popular_guides=popular_guides,
        current_page=page,
        total_pages=total_pages
    )

@guide_blueprint.route('/<int:guide_id>')
def guide_detail(guide_id):
    """공략 세부 페이지"""
    # SQLAlchemy 세션 사용
    db_session = SessionLocal()
    guide = db_session.query(Guide).get(guide_id)

    if not guide:
        db_session.close()
        return "Guide not found", 404  # 공략이 없다면 404 오류를 반환

    # 로그인된 사용자 정보 가져오기
    user_id = session.get('user_id')  # 로그인된 사용자 ID
    username = get_user_info(user_id)  # Redis에서 사용자 이름 가져오기

    # 공략 작성자의 이름 가져오기
    guide.author_name = get_user_info(guide.user_id)
    db_session.close()

    return render_template(
        'guide_detail.html',
        guide=guide,
        user_id=user_id,
        username=username
    )

#  공략 등록
@guide_blueprint.route('/create', methods=['GET', 'POST'], endpoint='create_guide')
@login_required
def create_guide():
    if request.method == 'POST':
        title = request.form.get('title')
        category_id = request.form.get('category_id')  # 선택된 카테고리 ID
        content = request.form.get('content')
        user_id = session.get('user_id')

        if not title or not content or not category_id:
            flash("모든 필드를 입력해야 합니다.", "danger")
            return redirect(url_for('guide.create_guide'))

        # 새로운 Guide 객체 생성
        new_guide = Guide(
            title=title,
            content=content,
            category_id=int(category_id),  # 카테고리 ID 저장
            user_id=user_id
        )
        db_session.add(new_guide)
        db_session.commit()

        flash("공략이 성공적으로 등록되었습니다.", "success")
        return redirect(url_for('guide.guide_list'))

    # 게임 카테고리 목록 조회
    categories = db_session.query(GameCategory).all()
    return render_template('create_guide.html', categories=categories)

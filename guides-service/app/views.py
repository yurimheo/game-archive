import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash, g
import requests
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from app.models import db_session, Guide, GameCategory, GuideComments

# SQLAlchemy 세션 설정
DATABASE_URI = "mysql+pymysql://admin:admin@mysql:3306/game_archive"
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 블루프린트 생성
guide_blueprint = Blueprint('guide', __name__)

AUTH_SERVICE_URL = "http://auth-service:5006"  # auth-service URL 설정

# 작성자 이름 가져오기
SECRET_KEY = "supersecretkey"
def fetch_author_name(user_id):
    """
    Auth 서비스에서 사용자 이름 가져오기
    """
    if not user_id:
        return "익명 사용자"

    try:
        url = f"{AUTH_SERVICE_URL}/users/{user_id}"  # 올바른 URL로 수정
        print(f"[DEBUG] Fetching user from URL: {url}")
        response = requests.get(url)

        if response.status_code == 200:
            user_data = response.json()
            username = user_data.get("username", "익명 사용자")
            print(f"[DEBUG] Fetched Username: {username}")
            return username
        else:
            print(f"[ERROR] Failed to fetch user {user_id}. Status: {response.status_code}, Response: {response.text}")
            return "익명 사용자"
    except requests.RequestException as e:
        print(f"[ERROR] Exception while fetching user {user_id}: {e}")
        return "익명 사용자"
    
# 공략 목록 페이지
@guide_blueprint.route('/')
def guide_list():
    page = request.args.get('page', 1, type=int)
    per_page = 10

    # 공략 목록 가져오기 (최신순)
    guides_query = db_session.query(Guide).order_by(desc(Guide.created_at))
    total_items = guides_query.count()
    total_pages = (total_items + per_page - 1) // per_page
    guides = guides_query.offset((page - 1) * per_page).limit(per_page).all()

    # 인기 공략 가져오기 (조회수 기준 상위 3개)
    popular_guides = (
        db_session.query(Guide)
        .order_by(desc(Guide.views))
        .limit(3)
        .all()
    )

    # 작성자 이름 가져오기
    for guide in guides:
        guide.author_name = fetch_author_name(guide.user_id)
    for guide in popular_guides:
        guide.author_name = fetch_author_name(guide.user_id)

    return render_template(
        'guide.html',
        guides=guides,
        popular_guides=popular_guides,  # 인기 공략 전달
        current_page=page,
        total_pages=total_pages,
        user=g.user  # 템플릿으로 사용자 정보 전달
    )


# 공략 세부 페이지
@guide_blueprint.route('/<int:guide_id>', methods=['GET', 'POST'])
def guide_detail(guide_id):
    """
    공략 세부 페이지
    """
    db_session = SessionLocal()
    guide = db_session.query(Guide).get(guide_id)

    if not guide:
        db_session.close()
        return "Guide not found", 404

    # 조회수 증가 로직
    try:
        guide.views += 1  # 조회수 1 증가
        db_session.commit()
    except Exception as e:
        logging.error(f"조회수 증가 중 오류 발생: {e}")
        db_session.rollback()

    # 댓글 조회
    comments = db_session.query(GuideComments).filter_by(guide_id=guide_id).order_by(GuideComments.created_at).all()

    # 댓글 작성자 이름 설정
    for comment in comments:
        comment.author_name = fetch_author_name(comment.user_id)

    # 공략 작성자의 이름 설정
    guide.author_name = fetch_author_name(guide.user_id)

    # 댓글 등록 처리
    if request.method == 'POST':
        if not g.user:
            flash("댓글을 등록하려면 로그인해야 합니다.", "danger")
            return redirect(url_for('auth.login'))

        content = request.form.get('content')  # 댓글 내용 가져오기
        if not content:
            flash("댓글 내용을 입력하세요.", "danger")
            return redirect(url_for('guide.guide_detail', guide_id=guide_id))

        try:
            # 댓글 생성
            new_comment = GuideComments(
                guide_id=guide_id,
                user_id=g.user["user_id"],
                content=content
            )
            db_session.add(new_comment)
            db_session.commit()
            flash("댓글이 성공적으로 등록되었습니다.", "success")
        except Exception as e:
            db_session.rollback()
            logging.error(f"댓글 등록 중 오류 발생: {e}")
            flash("댓글 등록에 실패했습니다.", "danger")
        finally:
            return redirect(url_for('guide.guide_detail', guide_id=guide_id))

    db_session.close()

    return render_template(
        'guide_detail.html',
        guide=guide,
        comments=comments,
        user=g.user
    )

# 공략 등록
@guide_blueprint.route('/create', methods=['GET', 'POST'])
def create_guide():
    if not g.user:
        flash("공략을 등록하려면 로그인해야 합니다.", "danger")
        return redirect("http://127.0.0.1:5006/login")

    if request.method == 'POST':
        title = request.form.get('title')
        category_id = request.form.get('category_id')
        content = request.form.get('content')

        if not title or not content or not category_id:
            flash("모든 필드를 입력해야 합니다.", "danger")
            return redirect(url_for('guide.create_guide'))

        try:
            # 새로운 Guide 객체 생성
            new_guide = Guide(
                title=title,
                content=content,
                category_id=int(category_id),
                user_id=g.user["user_id"]
            )
            db_session.add(new_guide)
            db_session.commit()
            flash("공략이 성공적으로 등록되었습니다.", "success")
            return redirect(url_for('guide.guide_list'))
        except Exception as e:
            db_session.rollback()
            logging.error(f"공략 등록 중 오류 발생: {e}")
            flash("공략 등록에 실패했습니다.", "danger")

    categories = db_session.query(GameCategory).all()
    return render_template('create_guide.html', categories=categories, user=g.user)

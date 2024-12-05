from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from app.models import db_session, News, NewsComments
from sqlalchemy import desc

# 블루프린트 생성
news_blueprint = Blueprint('news', __name__)

@news_blueprint.route('/')
def news_list():
    """
    뉴스 목록 페이지
    """
    page = request.args.get('page', 1, type=int)
    per_page = 6

    # 뉴스 데이터를 가져와 페이지네이션 처리
    news_query = db_session.query(News).order_by(desc(News.created_at))
    total_items = news_query.count()
    total_pages = (total_items + per_page - 1) // per_page
    news_items = news_query.offset((page - 1) * per_page).limit(per_page).all()

    # 인기 뉴스 조회 (조회수 기준 상위 3개)
    popular_news = db_session.query(News).order_by(desc(News.views)).limit(3).all()

    # 뉴스 리스트 데이터 구성
    news_list = [
        {
            "news_id": news.news_id,
            "title": news.title,
            "image_url": news.image_path or "images/default_news.jpg",  # 기본 이미지 경로 포함
            "date": news.created_at.strftime("%Y. %m. %d."),
        }
        for news in news_items
    ]

    # 인기 뉴스 데이터 구성
    popular_news_list = [
        {
            "news_id": news.news_id,
            "title": news.title,
            "date": news.created_at.strftime("%Y. %m. %d."),
        }
        for news in popular_news
    ]

    return render_template(
        'news.html',
        news_list=news_list,
        popular_news_list=popular_news_list,
        current_page=page,
        total_pages=total_pages,
        current_user=g.user  # 현재 로그인 사용자 전달
    )

@news_blueprint.route('/<int:news_id>')
def news_detail(news_id):
    """
    뉴스 세부 페이지
    """
    news_item = db_session.query(News).get(news_id)

    if not news_item:
        flash("해당 뉴스는 존재하지 않습니다.", "danger")
        return redirect(url_for('news.news_list'))

    try:
        # 조회수 증가
        news_item.views += 1
        db_session.commit()
    except Exception:
        db_session.rollback()
        flash("조회수 증가 중 오류가 발생했습니다.", "danger")

    return render_template(
        'news_detail.html',
        news=news_item,
        current_user=g.user  # 현재 로그인 사용자 전달
    )

@news_blueprint.route('/<int:news_id>/comment', methods=['POST'])
def add_comment(news_id):
    """
    뉴스 댓글 추가
    """
    # 로그인 여부 확인
    if g.user is None:
        flash("댓글을 작성하려면 로그인이 필요합니다.", "warning")
        return redirect("http://127.0.0.1:5006/login")  # 로그인 페이지로 이동

    news_item = db_session.query(News).get(news_id)
    if not news_item:
        flash("해당 뉴스는 존재하지 않습니다.", "danger")
        return redirect(url_for('news.news_list'))

    # 댓글 데이터 가져오기
    comment_content = request.form.get('comment', '').strip()
    if not comment_content:
        flash("댓글 내용을 입력해주세요.", "warning")
        return redirect(url_for('news.news_detail', news_id=news_id))

    if len(comment_content) > 500:
        flash("댓글은 500자 이하로 작성해주세요.", "warning")
        return redirect(url_for('news.news_detail', news_id=news_id))

    try:
        # 댓글 추가 (현재 로그인한 사용자의 이름을 작성자로 저장)
        new_comment = NewsComments(
            news_id=news_id,
            content=comment_content,
            author=g.user['username']  # g.user에서 사용자 이름 가져오기
        )
        db_session.add(new_comment)
        db_session.commit()
        flash("댓글이 등록되었습니다.", "success")
    except Exception as e:
        db_session.rollback()
        flash(f"댓글 등록 중 오류가 발생했습니다: {str(e)}", "danger")

    return redirect(url_for('news.news_detail', news_id=news_id))

import logging
import requests
from flask import Blueprint, jsonify, request, g
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from app.models import News, Base
import jwt as pyjwt

# JWT 설정
SECRET_KEY = "supersecretkey"

# 데이터베이스 연결 설정
DATABASE_URI = "mysql+pymysql://admin:admin@mysql:3306/game_archive"
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 블루프린트 생성
news_blueprint = Blueprint('news', __name__, url_prefix='/news')

# JWT 검증 로직
@news_blueprint.before_app_request
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

# 뉴스 목록 API
@news_blueprint.route('/', methods=['GET'])
def get_news():
    session = SessionLocal()
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 10

        # 뉴스 데이터 가져오기 (최신순)
        news_query = session.query(News).order_by(desc(News.created_at))
        total_items = news_query.count()
        total_pages = (total_items + per_page - 1) // per_page
        news_list = news_query.offset((page - 1) * per_page).limit(per_page).all()

        # 데이터 응답
        result = [
            {
                "news_id": news.news_id,
                "title": news.title,
                "content": news.content,
                "views": news.views,
                "image_path": news.image_path,
                "author": g.user.get("username") if g.user and news.user_id == g.user.get("user_id") else "알 수 없음",
                "created_at": news.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            }
            for news in news_list
        ]
        return jsonify({
            "total_items": total_items,
            "total_pages": total_pages,
            "news": result
        }), 200
    except Exception as e:
        logging.error(f"Error fetching news: {e}")
        return jsonify({"error": "뉴스를 가져오는 중 오류가 발생했습니다."}), 500
    finally:
        session.close()

# 뉴스 상세보기 API (조회수 증가)
@news_blueprint.route('/<int:news_id>', methods=['GET'])
def get_news_detail(news_id):
    session = SessionLocal()
    try:
        news = session.query(News).get(news_id)
        if not news:
            return jsonify({"error": "뉴스를 찾을 수 없습니다."}), 404

        # 조회수 증가
        news.views += 1
        session.commit()

        result = {
            "news_id": news.news_id,
            "title": news.title,
            "content": news.content,
            "views": news.views,
            "image_path": news.image_path,
            "author": g.user.get("username") if g.user and news.user_id == g.user.get("user_id") else "알 수 없음",
            "created_at": news.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
        return jsonify(result), 200
    except Exception as e:
        session.rollback()
        logging.error(f"Error fetching news detail: {e}")
        return jsonify({"error": "뉴스 상세 정보를 가져오는 중 오류가 발생했습니다."}), 500
    finally:
        session.close()

# 뉴스 생성 API
@news_blueprint.route('/create', methods=['POST'])
def create_news():
    if not g.user:
        return jsonify({"error": "로그인이 필요합니다."}), 401

    title = request.json.get('title')
    content = request.json.get('content')
    image_path = request.json.get('image_path')  # 이미지 경로
    user_id = g.user.get('user_id')

    if not title or not content:
        return jsonify({"error": "제목과 내용을 입력하세요."}), 400

    session = SessionLocal()
    try:
        new_news = News(
            title=title,
            content=content,
            image_path=image_path,
            user_id=user_id
        )
        session.add(new_news)
        session.commit()
        return jsonify({"message": "뉴스가 성공적으로 등록되었습니다."}), 201
    except Exception as e:
        session.rollback()
        logging.error(f"Error creating news: {e}")
        return jsonify({"error": "뉴스를 생성하는 중 오류가 발생했습니다."}), 500
    finally:
        session.close()

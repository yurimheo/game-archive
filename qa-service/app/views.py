import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from app.models import SessionLocal, Question, Answer
from sqlalchemy.orm import joinedload
import jwt as pyjwt

qa_blueprint = Blueprint(
    'qa',
    __name__,
    template_folder='app/templates',
    static_folder='app/static'
)

COMMON_SERVICE_URL = "http://127.0.0.1:5001"  # common-service의 URL
AUTH_SERVICE_URL = "http://auth-service:5006"  # auth-service의 URL

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

# 질문 목록 페이지
@qa_blueprint.route('/qa')
def index():
    session = SessionLocal()
    questions = []
    popular_questions = []
    try:
        questions = session.query(Question).order_by(Question.question_id.desc()).all()
        popular_questions = session.query(Question).order_by(Question.views.desc()).limit(3).all()

        # 사용자 정보 가져오기
        question_data = []
        for question in questions:
            author_name = fetch_author_name(question.user_id)
            question_data.append({
                "question_id": question.question_id,
                "title": question.title,
                "views": question.views,
                "author_name": author_name
            })
            print(f"[DEBUG] Question ID: {question.question_id}, Author: {author_name}")
    except Exception as e:
        session.rollback()
        print(f"[ERROR] Error fetching questions: {e}")
        flash(f"데이터를 불러오는 중 오류가 발생했습니다: {e}", 'danger')
    finally:
        session.close()

    # 페이지네이션
    current_page = int(request.args.get('page', 1))
    page_size = 5
    offset = (current_page - 1) * page_size
    total_pages = (len(question_data) + page_size - 1) // page_size

    # 템플릿으로 전달된 데이터를 확인합니다.
    print(f"[DEBUG] Questions to Template: {question_data[offset:offset + page_size]}")
    return render_template(
        'qa.html',
        popular_questions=popular_questions,
        questions=question_data[offset:offset + page_size],
        current_page=current_page,
        total_pages=total_pages
    )

# 질문 등록 페이지
@qa_blueprint.route('/qa/create', methods=['GET', 'POST'])
def create():
    session_db = SessionLocal()

    # JWT 토큰 인증 확인
    token = request.cookies.get("access_token")
    if not token:
        flash("로그인이 필요합니다.", 'danger')
        return redirect("http://127.0.0.1:5006/login")

    try:
        decoded_token = pyjwt.decode(
            token,
            key="supersecretkey",  # 실제 SECRET_KEY를 사용
            algorithms=["HS256"]
        )
        user_id = decoded_token.get("user_id")
        username = decoded_token.get("username")
        g.user = {"user_id": user_id, "username": username}
    except (pyjwt.ExpiredSignatureError, pyjwt.InvalidTokenError):
        flash("로그인 세션이 만료되었습니다. 다시 로그인하세요.", 'warning')
        return redirect("http://127.0.0.1:5006/login")

    if request.method == 'POST':
        # 폼 데이터 처리
        title = request.form.get('title')
        content = request.form.get('content')

        if not user_id:
            flash("로그인이 필요합니다.", 'danger')
            return redirect("http://127.0.0.1:5006/login")

        # 새 질문 데이터베이스에 저장
        new_question = Question(title=title, content=content, user_id=user_id)
        session_db.add(new_question)
        session_db.commit()

        flash(f"'{title}' 질문이 성공적으로 등록되었습니다!", 'success')
        session_db.close()
        return redirect(url_for('qa.index'))

    return render_template('qa-create.html', user=g.user)

# 질문 상세 페이지 (답변 작성 포함)
@qa_blueprint.route('/qa/<int:question_id>', methods=['GET', 'POST'])
def detail(question_id):
    session_db = SessionLocal()

    # 질문 조회
    question = session_db.query(Question).filter(Question.question_id == question_id).first()

    if not question:
        session_db.close()
        flash("질문을 찾을 수 없습니다.", 'danger')
        return redirect(url_for('qa.index'))

    if request.method == 'POST':
        # JWT 토큰 인증 확인
        token = request.cookies.get("access_token")
        if not token:
            flash("로그인이 필요합니다.", 'danger')
            return redirect("http://127.0.0.1:5006/login")

        try:
            decoded_token = pyjwt.decode(
                token,
                key="supersecretkey",  # 실제 SECRET_KEY를 사용
                algorithms=["HS256"]
            )
            user_id = decoded_token.get("user_id")
            username = decoded_token.get("username")
        except (pyjwt.ExpiredSignatureError, pyjwt.InvalidTokenError):
            flash("로그인 세션이 만료되었습니다. 다시 로그인하세요.", 'warning')
            return redirect("http://127.0.0.1:5006/login")

        # 폼 데이터 처리
        answer_content = request.form.get('answer_content', '').strip()
        if not answer_content:
            flash("답변 내용을 입력해주세요.", 'warning')
            return redirect(url_for('qa.detail', question_id=question_id))

        # 답변 저장
        new_answer = Answer(
            question_id=question_id,
            user_id=user_id,
            content=answer_content
        )
        session_db.add(new_answer)
        session_db.commit()
        flash("답변이 성공적으로 등록되었습니다.", 'success')

    # 질문 데이터 변환
    question_data = {
        "question_id": question.question_id,
        "title": question.title,
        "content": question.content,
        "views": question.views,
        "author_name": fetch_author_name(question.user_id),
        "created_at": question.created_at.strftime('%Y-%m-%d %H:%M:%S'),
    }

    # 답변 목록 조회 및 변환
    answers = session_db.query(Answer).filter(Answer.question_id == question_id).all()
    answer_data = [
        {
            "author_name": fetch_author_name(answer.user_id),
            "content": answer.content,
            "created_at": answer.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
        for answer in answers
    ]

    session_db.close()

    return render_template(
        'qa-detail.html',
        question=question_data,
        answers=answer_data
    )



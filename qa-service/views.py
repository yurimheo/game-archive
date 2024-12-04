import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import SessionLocal, Question

qa_blueprint = Blueprint(
    'qa',
    __name__,
    template_folder='app/templates',
    static_folder='app/static'
)

COMMON_SERVICE_URL = "http://127.0.0.1:5001"  # common-service의 URL

# 질문 목록 페이지
@qa_blueprint.route('/qa')
def index():
    session = SessionLocal()

    # 데이터베이스에서 질문 목록 조회
    questions = session.query(Question).order_by(Question.question_id.desc()).all()
    popular_questions = session.query(Question).order_by(Question.views.desc()).limit(3).all()

    session.close()

    # 페이지네이션 데이터
    current_page = int(request.args.get('page', 1))
    page_size = 5
    offset = (current_page - 1) * page_size
    total_pages = (len(questions) + page_size - 1) // page_size

    return render_template(
        'qa.html',
        popular_questions=popular_questions,
        questions=questions[offset:offset + page_size],
        current_page=current_page,
        total_pages=total_pages
    )

# 질문 등록 페이지
@qa_blueprint.route('/qa/create', methods=['GET', 'POST'])
def create():
    session_db = SessionLocal()

    if request.method == 'POST':
        # 폼 데이터 처리
        title = request.form.get('title')
        content = request.form.get('content')

        # 실제 로그인된 사용자 ID를 가져옴
        user_id = session.get('user_id', None)
        if not user_id:
            flash("로그인이 필요합니다.", 'danger')
            return redirect(url_for('auth.login'))  # 로그인 페이지로 리다이렉트

        # 새 질문 데이터베이스에 저장
        new_question = Question(title=title, content=content, user_id=user_id)
        session_db.add(new_question)
        session_db.commit()

        flash(f"'{title}' 질문이 성공적으로 등록되었습니다!", 'success')
        session_db.close()
        return redirect(url_for('qa.index'))

    return render_template('qa-create.html')

# 질문 상세 페이지
@qa_blueprint.route('/qa/<int:question_id>')
def detail(question_id):
    session_db = SessionLocal()

    # 질문 조회
    question = session_db.query(Question).filter(Question.question_id == question_id).first()

    if not question:
        session_db.close()
        flash("질문을 찾을 수 없습니다.", 'danger')
        return redirect(url_for('qa.index'))

    # 조회수 증가
    question.views += 1
    session_db.commit()

    # API 호출로 작성자 이름 가져오기
    user_name = "알 수 없는 사용자"
    try:
        response = requests.get(f"{COMMON_SERVICE_URL}/api/users/{question.user_id}")
        if response.status_code == 200:
            user_data = response.json()
            user_name = user_data.get("username", "알 수 없는 사용자")
    except requests.RequestException:
        user_name = "알 수 없는 사용자"

    session_db.close()

    return render_template(
        'qa-detail.html',
        question={
            "title": question.title,
            "content": question.content,
            "views": question.views,
            "user_id": question.user_id
        },
        user_name=user_name
    )

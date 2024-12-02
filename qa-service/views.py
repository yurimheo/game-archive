from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import SessionLocal, Question

qa_blueprint = Blueprint(
    'qa',
    __name__,
    template_folder='app/templates',
    static_folder='app/static'
)

# 질문 목록 페이지
@qa_blueprint.route('/qa')
def index():
    session = SessionLocal()

    # 데이터베이스에서 질문 목록 조회
    questions = session.query(Question).order_by(Question.id.desc()).all()
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
    session = SessionLocal()

    if request.method == 'POST':
        # 폼 데이터 처리
        title = request.form.get('title')
        content = request.form.get('content')
        author = "사용자1"  # 예제, 실제 서비스에서는 로그인된 사용자 정보 활용

        # 새 질문 데이터베이스에 저장
        new_question = Question(title=title, content=content, author=author)
        session.add(new_question)
        session.commit()

        flash(f"'{title}' 질문이 성공적으로 등록되었습니다!", 'success')
        session.close()
        return redirect(url_for('qa.index'))

    return render_template('qa-create.html')

# 질문 상세 페이지
@qa_blueprint.route('/qa/<int:question_id>')
def detail(question_id):
    session = SessionLocal()

    # 데이터베이스에서 질문 조회
    question = session.query(Question).filter(Question.id == question_id).first()

    # 조회수 증가
    if question:
        question.views += 1
        session.commit()

    session.close()

    return render_template('qa-detail.html', question=question)

from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Question, User  # User 모델 추가

# 블루프린트 정의
qa_blueprint = Blueprint(
    'qa',
    __name__,
    template_folder='app/templates',
    static_folder='app/static'
)

# 질문 목록 페이지
@qa_blueprint.route('/')
def index():
    # 현재 페이지 번호
    page = request.args.get('page', 1, type=int)
    per_page = 10  # 페이지당 질문 수

    # 질문 목록 및 인기 질문 가져오기
    questions_paginated = db.session.query(Question, User.username).join(User).order_by(Question.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    questions = questions_paginated.items
    total_pages = questions_paginated.pages
    current_page = questions_paginated.page

    # 인기 질문 (예: 조회수가 높은 질문 상위 5개)
    popular_questions = db.session.query(Question, User.username).join(User).order_by(Question.updated_at.desc()).limit(5).all()

    return render_template(
        'qa.html',
        questions=questions,
        popular_questions=popular_questions,
        current_page=current_page,
        total_pages=total_pages
    )
    
# 질문 상세 페이지
@qa_blueprint.route('/<int:question_id>')
def detail(question_id):
    # 질문과 사용자 정보를 가져오기
    question = db.session.query(Question, User).join(User).filter(Question.question_id == question_id).first_or_404()
    
    # question[0]은 Question 객체, question[1]은 User 객체
    return render_template('qa-detail.html', question=question[0], username=question[1].username)



# 질문 등록 페이지
@qa_blueprint.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # 폼 데이터 처리
        title = request.form.get('title')
        content = request.form.get('content')

        # 예: 현재 로그인한 사용자 ID
        user_id = 1  # 임시값, 실제로는 로그인한 사용자 ID로 설정해야 함

        # 사용자가 존재하는지 확인
        user = User.query.get(user_id)
        if not user:
            flash("유효하지 않은 사용자입니다.", "error")
            return redirect(url_for('qa.create'))
        
        # 새로운 질문 객체 생성
        new_question = Question(title=title, content=content, user_id=user_id)
        
        # 데이터베이스에 추가 및 커밋
        db.session.add(new_question)
        db.session.commit()

        # 플래시 메시지 표시 후 질문 목록으로 리디렉션
        flash(f"'{title}' 질문이 성공적으로 등록되었습니다!", 'success')
        return redirect(url_for('qa.index'))

    # GET 요청 시 등록 폼 렌더링
    return render_template('qa-create.html')
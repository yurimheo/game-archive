from flask import Blueprint, render_template, request, redirect, url_for, flash

# 블루프린트 정의
qa_blueprint = Blueprint(
    'qa',
    __name__,
    template_folder='app/templates',  # 템플릿 경로
    static_folder='app/static'        # 정적 파일 경로
)


# 질문 목록 페이지
@qa_blueprint.route('/qa')
def index():
     # 인기 질문 데이터 예제
    popular_questions = [
        {"id": 101, "title": "게임 속성 변경 방법은?", "author": "PlayerOne", "views": 320},
        {"id": 102, "title": "최고의 캐릭터 빌드는?", "author": "GamerGirl", "views": 250},
        {"id": 103, "title": "서버 오류가 발생했어요. 해결법은?", "author": "TechMaster", "views": 190},
    ]


    # 예제 데이터
    questions = [
        {"id": 1, "title": "질문 제목 1", "author": "사용자1", "views": 150},
        {"id": 2, "title": "질문 제목 2", "author": "사용자2", "views": 120},
        {"id": 3, "title": "질문 제목 3", "author": "사용자3", "views": 95},
    ]

    # 페이지네이션 데이터
    current_page = int(request.args.get('page', 1))  # 기본값: 1
    total_pages = 5  # 전체 페이지 수

    return render_template(
        'qa.html',
        popular_questions=popular_questions,
        questions=questions,
        current_page=current_page,
        total_pages=total_pages
    )

# 질문 등록 페이지
@qa_blueprint.route('/qa/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # 폼 데이터 처리
        title = request.form.get('title')
        content = request.form.get('content')
        flash(f"'{title}' 질문이 성공적으로 등록되었습니다!", 'success')
        return redirect(url_for('qa.index'))

    # GET 요청 시 등록 폼 렌더링
    return render_template('qa-create.html')

# 질문 상세 페이지
@qa_blueprint.route('/qa/<int:question_id>')
def detail(question_id):
    # 예제 데이터
    question = {
        "id": question_id,
        "title": f"질문 제목 {question_id}",
        "author": "사용자1",
        "content": "이것은 질문 내용입니다.",
        "views": 123
    }
    return render_template('qa-detail.html', question=question)

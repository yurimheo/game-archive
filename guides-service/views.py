from flask import Blueprint, render_template, request, redirect, url_for, flash

# Blueprint 생성
bp = Blueprint('guide', __name__, url_prefix='/guide')

# 공략 게시판 메인 페이지
@bp.route('/')
def index():
    current_page = request.args.get('page', 1, type=int)
    guides_per_page = 10  # 한 페이지당 10개의 게시글
    total_guides = 100  # 전체 게시글 수 (임시값)
    total_pages = (total_guides + guides_per_page - 1) // guides_per_page

    start_index = (current_page - 1) * guides_per_page + 1
    end_index = min(start_index + guides_per_page - 1, total_guides)

    return render_template(
        'guide.html',
        current_page=current_page,
        total_pages=total_pages,
        start_index=start_index,
        end_index=end_index
    )

# 질문 등록 페이지
@bp.route('/submit_question', methods=['GET', 'POST'])
def submit_question():
    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        content = request.form['content']

        # 데이터베이스 저장 로직 추가 필요
        flash('질문이 성공적으로 등록되었습니다.')
        return redirect(url_for('guide.index'))

    return render_template('submit_question.html')

# 질문 상세 페이지
@bp.route('/guide_detail/<int:guide_id>')
def guide_detail(guide_id):
    # guide_id를 활용해 데이터베이스에서 조회할 수 있음
    return render_template(
        'guide_detail.html',
        guide_id=guide_id
    )

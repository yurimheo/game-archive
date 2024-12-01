from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user_table'

    # 필드 정의
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(45), unique=True, nullable=False)  # 아이디
    password = db.Column(db.String(100), nullable=False)  # 비밀번호
    email = db.Column(db.String(100), unique=True, nullable=False)  # 이메일
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())  # 생성일
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())  # 수정일
    last_login = db.Column(db.DateTime, nullable=True)  # 마지막 로그인 시간

    # 관계 정의
    questions = db.relationship('Question', backref='user', lazy=True)  # 질문 테이블과 관계
    guides = db.relationship('Guide', backref='user', lazy=True)  # 공략 테이블과 관계
    news = db.relationship('News', backref='user', lazy=True)  # 뉴스 테이블과 관계

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'<User {self.username}>'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import Column, BigInteger, Integer, String, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

# Base 클래스 정의
Base = declarative_base()

# 데이터베이스 연결 설정
DATABASE_URI = "mysql+pymysql://admin:admin@mysql:3306/game_archive"
engine = create_engine(DATABASE_URI)

# 세션 생성기
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Scoped session으로 설정
db_session = scoped_session(SessionLocal)

# 데이터베이스 초기화 함수
def init_db():
    Base.metadata.create_all(bind=engine)

# Guide 모델 정의
class Guide(Base):
    __tablename__ = 'Guide'

    guide_id = Column(BigInteger, primary_key=True, autoincrement=True)
    category_id = Column(BigInteger, nullable=False)
    user_id = Column(BigInteger, nullable=False)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    views = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

# Game Category 모델
class GameCategory(Base):
    __tablename__ = 'Game_Category'

    category_id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)

# Guide Comments 모델 정의
class GuideComments(Base):
    __tablename__ = 'Guide_Comments'

    comment_id = Column(BigInteger, primary_key=True, autoincrement=True)
    guide_id = Column(BigInteger, nullable=False)  # 공략 ID (외래 키로 연결 가능)
    user_id = Column(BigInteger, nullable=False)  # 작성자 ID
    content = Column(Text, nullable=False)  # 댓글 내용
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())  # 생성 시간
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())  # 수정 시간
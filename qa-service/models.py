from sqlalchemy import Column, BigInteger, Integer, String, Text, TIMESTAMP, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func


Base = declarative_base()

class Question(Base):
    __tablename__ = 'Question'

    question_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    views = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())  # MySQL CURRENT_TIMESTAMP 함수 사용
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    
# 데이터베이스 연결 설정
DATABASE_URI = "mysql+pymysql://admin:admin@mysql:3306/game_archive"

engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 데이터베이스 초기화 함수
def init_db():
    Base.metadata.create_all(bind=engine)

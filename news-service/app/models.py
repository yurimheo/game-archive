from sqlalchemy import Column, BigInteger, Integer, String, Text, TIMESTAMP, ForeignKey, func, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from datetime import datetime

Base = declarative_base()

# 데이터베이스 연결
DATABASE_URI = "mysql+pymysql://admin:admin@mysql:3306/game_archive"
engine = create_engine(DATABASE_URI)

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def init_db():
    Base.metadata.create_all(bind=engine)

class News(Base):
    __tablename__ = 'News'

    news_id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    views = Column(Integer, default=0)
    image_path = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False)

    # 관계 정의
    comments = relationship('NewsComments', back_populates='news')

class NewsComments(Base):
    __tablename__ = 'News_Comments'

    # 필드 정의
    comment_id = Column(BigInteger, primary_key=True, autoincrement=True)
    news_id = Column(BigInteger, ForeignKey('News.news_id'), nullable=False)
    author = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계 정의
    news = relationship('News', back_populates='comments')

# 파일을 직접 실행하면 데이터베이스 초기화
if __name__ == "__main__":
    init_db()
    print("데이터베이스 테이블이 생성되었습니다.")
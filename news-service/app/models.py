from sqlalchemy import Column, BigInteger, Integer, String, Text, TIMESTAMP, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

# 데이터베이스 연결
DATABASE_URI = "mysql+pymysql://admin:admin@mysql:3306/game_archive"
engine = create_engine(DATABASE_URI)

def init_db():
    Base.metadata.create_all(bind=engine)

class News(Base):
    __tablename__ = 'news'

    news_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('user.user_id'), nullable=False)  # User 테이블의 외래키
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    views = Column(Integer, default=0)
    image_path = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False)

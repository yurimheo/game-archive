from sqlalchemy import Column, BigInteger, String, DateTime, func, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

DATABASE_URI = "mysql+pymysql://admin:admin@mysql:3306/game_archive"  # 실제 MySQL 서버 정보
engine = create_engine(DATABASE_URI)

# 세션 설정
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# User 테이블 정의
class User(Base):
    __tablename__ = 'users'

    user_id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

def init_db():
    Base.metadata.create_all(bind=engine)

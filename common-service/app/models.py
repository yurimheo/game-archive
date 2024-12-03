from sqlalchemy import Column, BigInteger, String, Text, Enum, TIMESTAMP, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Comment(Base):
    __tablename__ = 'comments'

    comment_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False)
    parent_table = Column(Enum('Guide_table', 'News_table', 'Question_table'), nullable=False)
    parent_id = Column(BigInteger, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=func.current_timestamp(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp(), nullable=False)

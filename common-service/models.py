from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin@mysql/flask_db'

db = SQLAlchemy(app)

# Content_table 모델 정의
class Content(db.Model):
    __tablename__ = 'Content_table'

    content_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    
# Comment_table 모델 정의
class Comment(db.Model):
    __tablename__ = 'Comment_table'

    comment_id = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey('Content_table.content_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User_table.user_id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
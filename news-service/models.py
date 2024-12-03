from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin@mysql/flask_db'

db = SQLAlchemy(app)

# News_table 모델 정의
class News(db.Model):
    __tablename__ = 'News_table'

    news_id = db.Column(db.Integer, primary_key=True)
    news_title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    auth = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
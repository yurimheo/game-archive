from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import models

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin@mysql-container/flask_db' # mysql-container == mysql이 들어있는 container의 name
    app.secret_key = 'my_secret_key_12345' #임시
    
    models.db.init_app(app)
     
    return app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app import db


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user_table'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(45), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    last_login = db.Column(db.DateTime, nullable=True)


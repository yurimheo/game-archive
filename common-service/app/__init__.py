from flask import Flask
from app.config import Config

def create_app():
    app = Flask(__name__,
                static_folder='static',
                template_folder='templates')

    return app

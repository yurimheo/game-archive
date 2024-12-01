from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'supersecretkey' 
    
    # 블루프린트 등록
    from .views import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app

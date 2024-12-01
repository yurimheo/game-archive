from flask import Flask
from views import bp as guide_bp  # views.py에서 Blueprint 가져오기

# Flask 앱 생성
app = Flask(__name__,
            static_folder='app/static',
            template_folder='app/templates')

# Blueprint 등록
app.register_blueprint(guide_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)

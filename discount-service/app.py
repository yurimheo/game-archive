from flask import Flask
from views import bp as discounts_bp  # views.py에서 블루프린트 가져오기
import logging

# Flask 앱 생성
app = Flask(__name__,
            static_folder='app/static',
            template_folder='app/templates')

# 로깅 설정
logging.basicConfig(level=logging.INFO)

# 블루프린트 등록
app.register_blueprint(discounts_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)

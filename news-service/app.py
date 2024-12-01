from app import create_app
from views import news_blueprint  # views.py에서 블루프린트 가져오기

app = create_app()

# 블루프린트 등록
app.register_blueprint(news_blueprint)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)

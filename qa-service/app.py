from app import create_app
from views import qa_blueprint  # views.py를 import

app = create_app()

# 블루프린트 등록
app.register_blueprint(qa_blueprint)

if __name__ == "__main__":
    print(app.url_map)  # URL 매핑 출력
    app.run(host="0.0.0.0", port=5005, debug=True)

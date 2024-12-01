from app import create_app, db
from flask_migrate import Migrate

# 애플리케이션 생성
app = create_app()

# Flask-Migrate 초기화
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006, debug=True)

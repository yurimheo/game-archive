from app import create_app

# Flask 앱 인스턴스 생성
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006)

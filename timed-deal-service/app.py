from app import create_app

# Flask 애플리케이션 생성
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5007, debug=True)

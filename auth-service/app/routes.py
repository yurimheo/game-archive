from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# 게이트웨이 메인 페이지
@app.route('/')
def main_page():
    # 각 서비스에서 데이터 가져오기
    try:
        discounts = requests.get('http://discount-service/api/discounts').json()
        news = requests.get('http://news-service/api/news').json()
    except Exception as e:
        discounts = []
        news = []

    return render_template('main.html', discounts=discounts, news=news)

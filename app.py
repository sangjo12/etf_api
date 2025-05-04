import yfinance as yf
from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# 더미 ETF 리스트 (실제 연동 시 API나 DB에서 받아오도록 수정 가능)
etf_list = [
    'KODEX200',
    'KODEX 200타겟위클리커버드콜',
    'KODEX 금융고배당TOP10타겟위클리커버드콜'
]

# 실시간 ETF 수익률 데이터를 가져오는 함수
def get_etf_data(etf_symbol):
    try:
        # yfinance에서 주식/ETF 데이터 가져오기
        etf = yf.Ticker(etf_symbol)
        hist = etf.history(period="1d")  # 하루의 데이터를 가져옴
        return hist['Close'].iloc[-1]  # 마지막 종가를 반환
    except Exception as e:
        return None

@app.route('/etf-list', methods=['GET'])
def get_etf_list():
    etf_data = {}
    for etf in etf_list:
        # 각 ETF의 실시간 데이터 가져오기
        data = get_etf_data(etf)
        if data:
            etf_data[etf] = {
                'price': data
            }
        else:
            etf_data[etf] = {'price': 'Error fetching data'}
    return jsonify(etf_data)

# Render 배포를 위한 포트/호스트 설정
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Render는 PORT 환경변수를 지정함
    app.run(host='0.0.0.0', port=port)

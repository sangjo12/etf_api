from flask import Flask, request, jsonify
from flask_cors import CORS
import yfinance as yf
import pandas as pd
import math

app = Flask(__name__)
CORS(app)  # 모든 도메인에서의 접근을 허용

# ETF 리스트 정의
etf_list = [
    {"name": "KODEX 금융고배당TOP10타겟위클리커버드콜", "code": "498410.KS"},
    {"name": "KODEX 200", "code": "069500.KS"},
    {"name": "KODEX 200타겟위클리커버드콜", "code": "498400.KS"},
]

@app.route('/etf-list')
def get_etf_list():
    return jsonify(etf_list)

@app.route('/etf-data')
def get_etf_data():
    code = request.args.get('code')
    chart_type = request.args.get('chartType', 'daily')
    is_log = request.args.get('log', 'false').lower() == 'true'

    interval_map = {
        'daily': '1d',
        'weekly': '1wk',
        'monthly': '1mo'
    }

    interval = interval_map.get(chart_type, '1d')

    try:
        df = yf.download(code, period='6mo', interval=interval, progress=False)
        if df.empty:
            return jsonify([])

        df = df.dropna()
        df = df.tail(100)  # 최근 100개만 사용

        result = []
        for index, row in df.iterrows():
            open_price = row['Open']
            high_price = row['High']
            low_price = row['Low']
            close_price = row['Close']
            volume = row['Volume']

            if is_log:
                open_price = math.log(open_price) if open_price > 0 else 0
                high_price = math.log(high_price) if high_price > 0 else 0
                low_price = math.log(low_price) if low_price > 0 else 0
                close_price = math.log(close_price) if close_price > 0 else 0

            result.append({
                'date': index.strftime('%Y-%m-%d'),
                'open': round(open_price, 2),
                'high': round(high_price, 2),
                'low': round(low_price, 2),
                'close': round(close_price, 2),
                'volume': volume
            })

        return jsonify(result)

    except Exception as e:
        print('Error:', e)
        return jsonify({'error': str(e)}), 500

# ✅ 추가: 종가 기반 라인 차트용 API
@app.route('/etf-close-data')
def get_etf_close_data():
    code = request.args.get('code')
    chart_type = request.args.get('chartType', 'daily')
    is_log = request.args.get('log', 'false').lower() == 'true'

    interval_map = {
        'daily': '1d',
        'weekly': '1wk',
        'monthly': '1mo'
    }

    interval = interval_map.get(chart_type, '1d')

    try:
        df = yf.download(code, period='6mo', interval=interval, progress=False)
        if df.empty:
            return jsonify([])

        df = df.dropna()
        df = df.tail(100)
        df['Close'] = df['Close'].apply(lambda x: math.log(x) if is_log and x > 0 else x)
        df['MA20'] = df['Close'].rolling(window=20).mean()
        df['Volume'] = df['Volume']

        result = []
        for index, row in df.iterrows():
            result.append({
                'date': index.strftime('%Y-%m-%d'),
                'close': round(row['Close'], 2),
                'ma20': round(row['MA20'], 2) if not pd.isna(row['MA20']) else None,
                'volume': row['Volume']
            })

        return jsonify(result)

    except Exception as e:
        print('Error:', e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

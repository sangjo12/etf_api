from flask import Flask, jsonify, request
from flask_cors import CORS
import yfinance as yf
import datetime

app = Flask(__name__)
CORS(app)

# ETF 목록 데이터
etf_list = [
    {'name': 'KODEX 200', 'code': '069500'},
    {'name': 'KODEX 금융고배당TOP10타겟위클리커버드콜', 'code': '498410'},
    {'name': 'KODEX 200타겟위클리커버드콜', 'code': '498400'}
]

# ETF 리스트를 반환하는 엔드포인트
@app.route('/etf-list', methods=['GET'])
def get_etf_list():
    return jsonify(etf_list)

# ETF 데이터를 가져오는 엔드포인트
@app.route('/etf-data', methods=['GET'])
def get_etf_data():
    code = request.args.get('code')
    chartType = request.args.get('chartType')  # 차트 종류 (일간, 주간, 월간)

    if not code or not chartType:
        return jsonify({'error': 'Invalid request'}), 400

    # 시작일과 종료일을 기본으로 설정 (추후 Flutter에서 보내는 방식에 맞춰 수정)
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=365)  # 1년 전 데이터

    # '1d' = 일간 차트, '1wk' = 주간 차트, '1mo' = 월간 차트
    interval_map = {
        'daily': '1d',  # 일간 차트
        'weekly': '1wk',  # 주간 차트
        'monthly': '1mo'  # 월간 차트
    }

    interval = interval_map.get(chartType)
    if not interval:
        return jsonify({'error': 'Invalid chart type'}), 400

    # Yahoo Finance에서 ETF 데이터를 가져옵니다.
    try:
        etf_data = yf.download(code + '.KS', start=start_date, end=end_date, interval=interval)

        # 필요한 데이터만 추출하여 반환합니다.
        result = []
        for date, row in etf_data.iterrows():
            result.append({
                'date': date.strftime('%Y-%m-%d'),
                'open': row['Open'],
                'high': row['High'],
                'low': row['Low'],
                'close': row['Close'],
                'volume': row['Volume'],
            })

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

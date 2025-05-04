from flask import Flask, jsonify, request, send_file
import yfinance as yf
import matplotlib.pyplot as plt
import io
import datetime

app = Flask(__name__)

# 이름과 종목 코드 매핑
ETF_MAPPING = {
    'KODEX 금융고배당TOP10타겟위클리커버드콜': '498410.KS',
    'KODEX 200': '069500.KS',
    'KODEX 200타겟위클리커버드콜': '498400.KS'
}

@app.route('/etf-list', methods=['GET'])
def get_etf_list():
    return jsonify(list(ETF_MAPPING.keys()))

@app.route('/etf-chart', methods=['GET'])
def get_etf_chart():
    start = request.args.get('start')
    end = request.args.get('end')
    selected_etfs = request.args.get('etfs')

    if not start or not end or not selected_etfs:
        return jsonify({'error': 'Missing parameters'}), 400

    try:
        start_date = datetime.datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end, "%Y-%m-%d")
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    selected_names = selected_etfs.split(',')

    plt.figure(figsize=(10, 5))

    for name in selected_names:
        code = ETF_MAPPING.get(name)
        if not code:
            continue
        try:
            data = yf.download(code, start=start_date, end=end_date)
            if not data.empty:
                plt.plot(data.index, data['Adj Close'], label=name)
        except Exception as e:
            print(f"Error loading {name}: {e}")

    if plt.gca().has_data():
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title(f'Selected ETF Chart: {start} ~ {end}')
        plt.legend()
        plt.grid(True)

        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        return send_file(buf, mimetype='image/png')
    else:
        return jsonify({'error': 'No valid ETF data found'}), 400

if __name__ == '__main__':
    app.run(debug=True)

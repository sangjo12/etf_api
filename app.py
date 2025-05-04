from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yfinance as yf
import matplotlib.pyplot as plt
import io
import datetime

app = Flask(__name__)
CORS(app)  # 모든 출처에서 접근 허용

# ETF 이름과 코드 매핑
ETF_MAP = {
    'KODEX 200': '069500.KS',
    'KODEX 금융고배당TOP10타겟위클리커버드콜': '498410.KS',
    'KODEX 200타겟위클리커버드콜': '498400.KS',
}

@app.route("/etf-list", methods=["GET"])
def get_etf_list():
    etfs = [{'name': name, 'code': code} for name, code in ETF_MAP.items()]
    return jsonify(etfs)

@app.route("/etf-chart", methods=["POST"])
def etf_chart():
    data = request.json
    selected_etfs = data.get("etfs", [])
    start = data.get("start")
    end = data.get("end")

    if not selected_etfs or not start or not end:
        return jsonify({"error": "Invalid input"}), 400

    try:
        start_date = datetime.datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400

    plt.figure(figsize=(10, 6))

    for name in selected_etfs:
        code = ETF_MAP.get(name)
        if not code:
            continue
        df = yf.download(code, start=start, end=end)
        if df.empty:
            continue
        df['Return'] = df['Adj Close'] / df['Adj Close'].iloc[0] * 100
        plt.plot(df.index, df['Return'], label=name)

    plt.title("ETF 수익률 비교 (%)")
    plt.xlabel("날짜")
    plt.ylabel("수익률 (%)")
    plt.legend()
    plt.grid(True)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    return send_file(buf, mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True)

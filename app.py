from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yfinance as yf
import mplfinance as mpf
import io
import datetime

app = Flask(__name__)
CORS(app)

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
    interval = data.get("interval", "1d")  # '1d', '1wk', '1mo'

    if not selected_etfs or not start or not end:
        return jsonify({"error": "Invalid input"}), 400

    try:
        start_date = datetime.datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400

    # 현재는 하나만 보여주는 것으로 제한 (봉차트는 한 종목씩 그리는 것이 일반적)
    etf_name = selected_etfs[0]
    code = ETF_MAP.get(etf_name)
    if not code:
        return jsonify({"error": "Invalid ETF name"}), 400

    df = yf.download(code, start=start, end=end, interval=interval)
    if df.empty:
        return jsonify({"error": "No data found"}), 404

    df.index.name = 'Date'

    buf = io.BytesIO()
    mpf.plot(
        df,
        type='candle',
        style='charles',
        title=f"{etf_name} ({interval} 차트)",
        ylabel='가격 (KRW)',
        ylabel_lower='Volume',
        volume=True,
        mav=(5, 20),
        datetime_format='%Y-%m-%d',
        tight_layout=True,
        savefig=buf
    )
    buf.seek(0)

    return send_file(buf, mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True)

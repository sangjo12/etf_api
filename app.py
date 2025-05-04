# ----------------------
# 서버 (app.py)
# ----------------------
from flask import Flask, request, jsonify
from flask_cors import CORS
import yfinance as yf
import pandas as pd

app = Flask(__name__)
CORS(app)

ETF_LIST = [
    {"name": "KODEX 200", "code": "069500.KS"},
    {"name": "KODEX 금융고배당TOP10타겟위클리커버드콜", "code": "498410.KS"},
    {"name": "KODEX 200타겟위클리커버드콜", "code": "498400.KS"},
]

@app.route("/etf-list")
def get_etf_list():
    return jsonify(ETF_LIST)

@app.route("/etf-data")
def get_etf_data():
    code = request.args.get("code")
    chart_type = request.args.get("chartType", "daily")

    if not code:
        return jsonify({"error": "code required"}), 400

    period_map = {
        "daily": ("1d", "6mo"),
        "weekly": ("1wk", "2y"),
        "monthly": ("1mo", "5y"),
    }

    interval, period = period_map.get(chart_type, ("1d", "6mo"))

    try:
        ticker = yf.Ticker(code)
        df = ticker.history(period=period, interval=interval)
        df = df.dropna()
        df.reset_index(inplace=True)
        df["Date"] = df["Date"].astype(str)

        chart_data = [
            {
                "date": row["Date"],
                "open": round(row["Open"], 2),
                "high": round(row["High"], 2),
                "low": round(row["Low"], 2),
                "close": round(row["Close"], 2),
            }
            for _, row in df.iterrows()
        ]

        return jsonify(chart_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

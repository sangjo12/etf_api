from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Flutter Web/App에서도 호출 가능하도록 CORS 허용

@app.route('/etf-list')
def etf_list():
    return jsonify([
        {"name": "KODEX200", "code": "069500"},
        {"name": "KODEX 금융고배당TOP10", "code": "310970"},
        {"name": "KODEX 200커버드콜", "code": "266370"}
    ])

if __name__ == '__main__':
    app.run()

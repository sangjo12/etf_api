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

@app.route('/etf-list', methods=['GET'])
def get_etf_list():
    return jsonify(etf_list)

# Render 배포를 위한 포트/호스트 설정
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Render는 PORT 환경변수를 지정함
    app.run(host='0.0.0.0', port=port)

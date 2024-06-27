from flask import Flask, request, jsonify
from business_logic.service import process_request

app = Flask(__name__)

@app.route('/api/request', methods=['POST'])
def handle_request():
    data = request.json
    result = process_request(data)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)

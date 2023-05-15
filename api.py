from flask import Flask, jsonify, request
import os

app = Flask(__name__)


@app.route('/')
def home():
    return "xRunda AI Lab"


@app.route('/api/data', methods=['GET', 'POST'])
def get_data():
    if request.method == 'GET':
        task_id = request.args.get('id')

        if not task_id:
            return jsonify({'code': 1001, 'msg': 'id is required'})

        sample_data = {
            'task_id': task_id,
            'data': [1, 2, 3, 4, 5]
        }
        return jsonify(sample_data)
    elif request.method == 'POST':
        print("DEBUG request", request)
        encode_url = request.args.get('url')

        if not encode_url:
            return jsonify({'code': 1001, 'msg': 'id is required'})

        response = {
            'submitted_url': encode_url,
            'summary': "summary",
        }

        return jsonify(response)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='127.0.0.1', port=port)

from flask import Flask, jsonify
from flask_cors import CORS
from data_processor import DataProcessor

app = Flask(__name__)
CORS(app)
processor = DataProcessor()

@app.route('/api/data/all', methods=['GET'])
def get_all_data():
    return jsonify(processor.unified_data)

@app.route('/api/data/<file_type>', methods=['GET'])
def get_specific_data(file_type):
    return jsonify(processor.get_data_by_type(file_type))

if __name__ == '__main__':
    app.run(debug=True)
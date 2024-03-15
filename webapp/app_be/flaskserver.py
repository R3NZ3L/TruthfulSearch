from flask import Flask, request
from flask import jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd

app = Flask(__name__)
CORS(app)

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {"message" : "Hello this is api end point"}
    filename = "covid_philippines"
    path = "datasets/" + filename + "/" + 'videos' + ".csv"
    dataset = pd.read_csv(path).drop("Unnamed: 0", axis=1)
    return dataset.to_json()


if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=105)
    app.run(host='0.0.0.0', port=105, debug=False)
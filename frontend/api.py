from flask import render_template, Flask, request, jsonify
from flask_cors import CORS
from frontend.api_methods import search
from time import time


app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app)


@app.route('/api/v1/search', methods=['GET'])
def hello_world():
    t1 = time()
    output = search(request.args['query'])
    print(output)
    t2 = time()
    print(t2 - t1)
    return jsonify(output)


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


app.run()

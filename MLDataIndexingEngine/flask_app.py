
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, jsonify
from Sparcsearch import SparcSearch
from WordCloud import Wordcloud
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

@app.route('/echo', methods=["POST", "GET"])
def echo():
    try:
        data = request.json
        print("Server: ", data)
        return data
    except Exception as e:
        raise e

@app.route('/sparcsearch', methods=["POST"])
def sparcsearch():
    try:
        data = request.json

        inputString = data["inputString"]
        fullModel = data["fullModel"]
        recommendation = data["recommendation"]

        jj, cs = SparcSearch(inputString, fullModel, recommendation)
        returnObject = {"topRanked": jj, "cs":cs}
        return jsonify(returnObject)
    except Exception as e:
        raise e

@app.route('/wordcloud', methods=["POST"])
def wordcloud():
    try:
        data = request.json

        sentences = data["sentences"]

        response = Wordcloud(sentences)
        returnObject = { "counters": response }
        return jsonify(returnObject)
    except Exception as e:
        raise e

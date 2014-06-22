#!/usr/bin/env python

from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/login', methods = ['POST'])
def login():
    return jsonify(request.get_json(force=True))

if __name__ == "__main__":
    app.run(debug=True)
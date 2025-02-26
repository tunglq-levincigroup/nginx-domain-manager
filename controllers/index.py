from flask import jsonify

def index_controller():
    respose = {"status": "running"}
    return jsonify(respose), 200
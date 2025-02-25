from flask import jsonify

def index_controller():
    return jsonify({"status": "running"}), 200
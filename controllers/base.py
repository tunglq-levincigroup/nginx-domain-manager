from flask import jsonify
import json
    
def get_request_data(data, *required_fields):
    instance = data
    if type(data) == 'str':
        instance = json.load(data)
    
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Missing fields in request body: {', '.join(missing_fields)}"}), 400
    return instance
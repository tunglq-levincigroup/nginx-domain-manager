from flask import jsonify

def api_response(statusCode: int, message: str, body = None):
    response = {
        message: message,
    } 
    if body:
        response['data'] = body  
    return jsonify(response), statusCode
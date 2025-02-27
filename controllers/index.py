from utils.response import api_response

def index_controller():
    data = {"status": "running"}
    return api_response(200, "OK", data)
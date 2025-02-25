from flask import Flask, jsonify, request
from controllers.base import *
from controllers.index import index_controller
from controllers.domain import add_domain_controller, edit_domain_controller, remove_domain_controller

app = Flask(__name__)

@app.get('/')
def index():
    return index_controller()

@app.post('/domain/add')
def add_domain():
    # auth_response = validate_api_key(request.headers)
    # if auth_response:
    #     return auth_response

    data = get_request_data(request.json, 'domain')
    if isinstance(data, tuple):
        return data

    return add_domain_controller(data.get('domain'))


@app.put('/domain/edit')
def edit_domain():
    # auth_response = validate_api_key(request.headers)
    # if auth_response:
    #     return auth_response

    data = get_request_data(request.json, 'old_domain', 'new_domain')
    if isinstance(data, tuple):
        return data

    return edit_domain_controller(data['old_domain'], data['new_domain'])


@app.delete('/domain/remove')
def remove_domain():
    # auth_response = validate_api_key(request.headers)
    # if auth_response:
    #     return auth_response

    data = get_request_data(request.json, 'domain')
    if isinstance(data, tuple):
        return data

    return remove_domain_controller(data['domain'])
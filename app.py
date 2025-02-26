from flask import Flask, request
from controllers.base import *
from controllers.index import *
from controllers.domain import *
from controllers.cname import *

app = Flask(__name__)

@app.get('/')
def index():
    return index_controller()

@app.post('/domain/add')
def add_domain():
    data = get_request_data(request.json, 'domain')
    if isinstance(data, tuple):
        return data

    return add_domain_controller(data.get('domain'))


@app.put('/domain/edit')
def edit_domain():
    data = get_request_data(request.json, 'old_domain', 'new_domain')
    if isinstance(data, tuple):
        return data

    return edit_domain_controller(data['old_domain'], data['new_domain'])


@app.delete('/domain/remove')
def remove_domain():
    data = get_request_data(request.json, 'domain')
    if isinstance(data, tuple):
        return data

    return remove_domain_controller(data['domain'])

@app.post('/cname/get-txt')
def get_txt():
    data = get_request_data(request.json, 'domain')
    if isinstance(data, tuple):
        return data

    return get_txt_controller(data['domain'])

@app.delete('/cname/validate-txt')
def validate_txt():
    data = get_request_data(request.json, 'domain')
    if isinstance(data, tuple):
        return data

    return apply_txt_controller(data['domain'])
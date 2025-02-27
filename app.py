from flask import Flask, request
from utils.request import get_request_data
from controllers.index import index_controller
from controllers.domain import add_domain_controller, edit_domain_controller, remove_domain_controller

app = Flask(__name__)

@app.get('/')
def index():
    return index_controller()

@app.post('/domain/add')
def add_domain():
    data = get_request_data(request.json, 'base-domain', 'domain')
    if isinstance(data, tuple):
        return data

    return add_domain_controller(data['base-domain'], data['domain'])

@app.put('/domain/edit')
def edit_alias():
    data = get_request_data(request.json, 'base-domain', 'old-domain', 'domain')
    if isinstance(data, tuple):
        return data

    return edit_domain_controller(data['base-domain'], data['old-domain'], data['domain'])

@app.delete('/domain/remove')
def remove_alias():
    data = get_request_data(request.json, 'domain')
    if isinstance(data, tuple):
        return data

    return remove_domain_controller(data['domain'])
from flask import Flask, request
from controllers.base import *
from controllers.index import *
from controllers.record import *

app = Flask(__name__)

@app.get('/')
def index():
    return index_controller()

@app.post('/record/get-txt')
def get_txt():
    data = get_request_data(request.json, 'domain')
    if isinstance(data, tuple):
        return data

    return get_txt_controller(data['domain'])

@app.post('/record/apply-txt')
def apply_txt():
    data = get_request_data(request.json, 'domain')
    if isinstance(data, tuple):
        return data

    return apply_txt_controller(data['domain'])

# @app.post('/domain/add-alias')
# def add_alias():
#     data = get_request_data(request.json, 'base-domain', 'domain')
#     if isinstance(data, tuple):
#         return data

#     return add_alias_controller(data['base-domain'], data['domain'])

# @app.put('/domain/edit-alias')
# def edit_alias():
#     data = get_request_data(request.json, 'base-domain', 'old-domain', 'domain')
#     if isinstance(data, tuple):
#         return data

#     return edit_alias_controller(data['base-domain'], data['old-domain'], data['domain'])

# @app.delete('/domain/remove-alias')
# def remove_alias():
#     data = get_request_data(request.json, 'domain')
#     if isinstance(data, tuple):
#         return data

#     return remove_alias_controller(data['domain'])
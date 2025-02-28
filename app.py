from flask import Flask, request
from utils.request import get_request_data
from utils.auth import authorize
from controllers.index import index_controller
from controllers.domain import (
    add_domain_controller,
    edit_domain_controller,
    remove_domain_controller,
)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    """Handle GET request to the root endpoint."""
    return index_controller()

@app.route('/domain/add', methods=['POST'])
def add_domain():
    """Handle POST request to add a new domain."""
    api_key = request.headers.get('X-API-KEY')
    status, message = authorize(api_key)
    if not status:
        return message, 401

    status, data = get_request_data(request.json, 'base_domain', 'domain')
    if not status:
        return data, 400

    return add_domain_controller(data['base_domain'], data['domain'])

@app.route('/domain/edit', methods=['PUT'])
def edit_domain():
    """Handle PUT request to edit an existing domain."""
    api_key = request.headers.get('X-API-KEY')
    status, message = authorize(api_key)
    if not status:
        return message, 401

    status, data = get_request_data(request.json, 'base_domain', 'old_domain', 'domain')
    if not status:
        return data, 400
    
    return edit_domain_controller(
        data['base_domain'], data['old_domain'], data['domain']
    )

@app.route('/domain/remove', methods=['DELETE'])
def remove_domain():
    """Handle DELETE request to remove a domain."""
    api_key = request.headers.get('X-API-KEY')
    status, message = authorize(api_key)
    if not status:
        return message, 401
    
    status, data = get_request_data(request.json, 'domain')
    if not status:
        return data, 400

    return remove_domain_controller(data['domain'])

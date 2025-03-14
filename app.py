from flask import Flask, request
from controllers.config import add_config_controller, remove_config_controller
from controllers.dns import check_dns_controller
from utils.request import get_request_data
from utils.response import api_response
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

#####################################################################
################    Register + redirect     #########################
#####################################################################
@app.route('/dns/check', methods=['POST'])
def check_dns():
    api_key = request.headers.get('X-API-KEY')
    status, message = authorize(api_key)
    if not status:
        return api_response(401, message)

    status, data = get_request_data(request.json, 'domains')
    if not status:
        return api_response(400, "Invalid parameters.")

    return check_dns_controller(data['domains'])

@app.route('/config/add', methods=['POST'])
def add_config():
    api_key = request.headers.get('X-API-KEY')
    status, message = authorize(api_key)
    if not status:
        return api_response(401, message)

    status, data = get_request_data(request.json, 'base_domain', 'redirect_domain', 'target_domain')
    if not status:
        return api_response(400, "Invalid parameters.")

    return add_config_controller(data['base_domain'], data['redirect_domain'], data['target_domain'])

@app.route('/config/remove', methods=['DELETE'])
def remove_config():
    api_key = request.headers.get('X-API-KEY')
    status, message = authorize(api_key)
    if not status:
        return api_response(401, message)
    
    status, data = get_request_data(request.json, 'target_domain')
    if not status:
        return api_response(400, "Invalid parameters.")

    return remove_config_controller(data['target_domain'])

################ This code is not up to date ########################
#####################################################################
################    Register                #########################
#####################################################################
@app.route('/domain/add', methods=['POST'])
def add_domain():
    """Handle POST request to add a new domain."""
    api_key = request.headers.get('X-API-KEY')
    status, message = authorize(api_key)
    if not status:
        return api_response(401, message)

    status, data = get_request_data(request.json, 'base_domain', 'domain')
    if not status:
        return api_response(400, "Invalid parameters.")

    return add_domain_controller(data['base_domain'], data['domain'])

@app.route('/domain/edit', methods=['PUT'])
def edit_domain():
    """Handle PUT request to edit an existing domain."""
    api_key = request.headers.get('X-API-KEY')
    status, message = authorize(api_key)
    if not status:
        return api_response(401, message)

    status, data = get_request_data(request.json, 'base_domain', 'old_domain', 'domain')
    if not status:
        return api_response(400, "Invalid parameters.")
    
    return edit_domain_controller(
        data['base_domain'], data['old_domain'], data['domain']
    )

@app.route('/domain/remove', methods=['DELETE'])
def remove_domain():
    """Handle DELETE request to remove a domain."""
    api_key = request.headers.get('X-API-KEY')
    status, message = authorize(api_key)
    if not status:
        return api_response(401, message)
    
    status, data = get_request_data(request.json, 'domain')
    if not status:
        return api_response(400, "Invalid parameters.")

    return remove_domain_controller(data['domain'])
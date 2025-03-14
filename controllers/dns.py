from services.nettools import pings
from utils.response import api_response
from utils.logger import error, info

def check_dns_controller(domains: list[str]):
    if not isinstance(domains, list) or not all(isinstance(domain, str) for domain in domains):
        return api_response(400, "Invalid input: 'domains' must be a list of strings.")

    if not domains:
        return api_response(400, "No domains provided.")

    ping_result, ping_message = pings(domains)
    if not ping_result:
        return api_response(400, ping_message)

    info(ping_message)
    return api_response(200, ping_message)
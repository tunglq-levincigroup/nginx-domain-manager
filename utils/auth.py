from utils.env import FLASK_API_KEY
from utils.logger import warn

def authorize(api_key):
    if api_key != FLASK_API_KEY:
        warn(f'Receive an Unauthorized request with api key = {api_key}')
        return False, "Unauthorized."
    return True, "Authorize successfully."
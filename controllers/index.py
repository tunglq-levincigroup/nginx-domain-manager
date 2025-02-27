from utils.response import api_response

def index_controller() -> dict:
    """
    Controller for the index route. Returns the API status.

    Returns:
        dict: A standard API response indicating the service status.
    """
    data = {"status": "running"}
    return api_response(200, "OK", data)

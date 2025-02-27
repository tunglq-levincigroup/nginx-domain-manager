from flask import jsonify
from typing import Optional, Any

def api_response(status_code: int, message: str, body: Optional[Any] = None) -> tuple:
    """
    Generates a standard API response.

    :param status_code: HTTP status code for the response
    :param message: Message to be included in the response
    :param body: Optional data to include in the response
    :return: Tuple containing JSON response and status code
    """
    response = {
        "message": message,
    }

    if body is not None:
        response["data"] = body

    return jsonify(response), status_code

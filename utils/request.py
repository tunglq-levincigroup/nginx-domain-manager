from flask import jsonify
import json
from typing import Any, Tuple, Union

def get_request_data(data: Union[dict, str], *required_fields: str) -> Tuple[bool, Union[dict, Any]]:
    """
    Parses and validates request data, checking for required fields.

    Args:
        data (Union[dict, str]): The incoming request data, either as a dict or a JSON string.
        *required_fields (str): Fields that must be present in the data.

    Returns:
        Tuple[bool, Union[dict, Any]]: Parsed data or an error response with status code.
    """
    try:
        instance = data if isinstance(data, dict) else json.loads(data)
    except json.JSONDecodeError:
        return False, {"error": "Invalid JSON format"}

    missing_fields = [field for field in required_fields if field not in instance]
    if missing_fields:
        return False, {"error": f"Missing fields in request body: {', '.join(missing_fields)}"}

    return True, instance

from services.env import FLASK_API_KEY

def authorize(api_key: str):
    print(api_key)
    print(FLASK_API_KEY)
    return api_key == FLASK_API_KEY
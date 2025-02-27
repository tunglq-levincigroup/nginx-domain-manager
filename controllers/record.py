from services.file import exist_domain
from services.acme import generate_txt_record, apply_txt_record
from utils.response import api_response

def get_txt_controller(domain: str):
    try:
        if exist_domain(domain):
            return api_response(400, "Domain existing.")
        
        txt, txt_message, txt_data = generate_txt_record(domain)
        if not txt:
            return api_response(400, txt_message)
        return api_response(200, txt_message, txt_data)
    except Exception as e:
        return api_response(400, f'Error while get txt record: {str(e)}')

def apply_txt_controller(domain: str):
    try:    
        if exist_domain(domain):
            return api_response(400, "Domain existing.")

        apply, apply_message = apply_txt_record(domain)
        if not apply:
            return api_response(400, apply_message)
        return api_response(200, apply_message)

    except Exception as e:
        return api_response(400, f'Error while apply txt record: {str(e)}')
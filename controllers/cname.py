from services.file import *
from services.template import *
from services.nginx import *
from services.nettools import *
from services.certbot import *
from ultils.response import api_response

def get_txt_controller(domain: str):
    try:
        if exist_file(domain):
            return api_response(400, "Domain existing.")
        
        txt, txt_message, txt_data = generate_txt_record(domain)
        if not txt:
            return api_response(400, txt_message)
        return api_response(txt, txt_message, txt_data)
    except Exception as e:
        return api_response(400, f'Error while get txt record: {str(e)}')
    
def apply_txt_controller(domain: str):
    try:
        if exist_file(domain):
            return 'Cannot add an exist domain.', 400

        run, run_message = continue_txt_record(domain)
        if not run:
            return api_response(400, run_message)

        return api_response(400, run_message)
    except Exception as e:
        return api_response(400, f'Error while apply txt record: {str(e)}')
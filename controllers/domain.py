from services.file import exist_domain, write_domain, remove_domain, backup_domain
from services.nginx import test_nginx, reload_nginx
from services.certbot import register_certbot
from services.nettools import ping
from utils.env import FLASK_BASE_URLS
from utils.response import api_response
from utils.logger import warn

def add_domain_controller(base_domain: str, domain: str):
    try:
        if base_domain not in FLASK_BASE_URLS:
            return api_response(400, "Base domain not found.")

        if exist_domain(domain):
            return api_response(400, "Domain existing.")
        
        ping_status, ping_message = ping(domain)
        if not ping_status:
            return api_response(400, ping_message)
        
        write, write_message = write_domain(domain)
        if not write:
            return api_response(400, write_message)
    
        test, test_message = test_nginx()
        if not test:
            return api_response(400, test_message)
    
        reload, reload_message = reload_nginx()
        if not reload:
            return api_response(400, reload_message)
        
        register, register_message = register_certbot(domain)
        if not register:
            return api_response(400, register_message)

        return api_response(200, "Add domain successfully")
    except Exception as e:
        return api_response(400, f'Error while get txt record: {str(e)}')

def edit_domain_controller(base_domain: str, old_domain: str, domain: str):
    try:
        if base_domain not in FLASK_BASE_URLS:
            return api_response(400, "Base domain not found.")

        if not exist_domain(old_domain):
            return api_response(400, "Old domain did not exist")

        if exist_domain(domain):
            return api_response(400, "Domain existing.")
        
        ping_status, ping_message = ping(domain)
        if not ping_status:
            return api_response(400, ping_message)
        
        write, write_message = write_domain(domain)
        if not write:
            return api_response(400, write_message)
    
        test, test_message = test_nginx()
        if not test:
            return api_response(400, test_message)
    
        reload, reload_message = reload_nginx()
        if not reload:
            return api_response(400, reload_message)
        
        register, register_message = register_certbot(domain)
        if not register:
            return api_response(400, register_message)

        backup, backup_message = backup_domain(domain)
        remove, remove_message = remove_domain(domain)
        if not backup or not remove:
            warn(backup_message)
            warn(remove_message)
        
        test, test_message = test_nginx()
        if not test:
            return api_response(400, test_message)
    
        reload, reload_message = reload_nginx()
        if not reload:
            return api_response(400, reload_message)

        return api_response(200, "Add domain successfully")
    except Exception as e:
        return api_response(400, f'Error while get txt record: {str(e)}')
    
def remove_domain_controller(domain: str):
    try:
        if not exist_domain(domain):
            return api_response(400, "Domain did not exist.")
        
        backup, backup_message = backup_domain(domain)
        if not backup:
            warn(backup_message)

        remove, remove_message = remove_domain(domain)
        if not remove:
            return api_response(400, remove_message)
    
        test, test_message = test_nginx()
        if not test:
            return api_response(400, test_message)
    
        reload, reload_message = reload_nginx()
        if not reload:
            return api_response(400, reload_message)

        return api_response(200, "Add domain successfully")
    except Exception as e:
        return api_response(400, f'Error while get txt record: {str(e)}')
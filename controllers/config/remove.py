from services.file import exist_domain, remove_domain, backup_domain
from services.nginx import test_nginx, reload_nginx
from utils.env import FLASK_BASE_URLS
from utils.response import api_response
from utils.logger import warn

def remove_config_controller(target_domain: str):
    try:
        # Check if the target_domain exists
        if not exist_domain(target_domain):
            return api_response(400, "Target domain does not exist.")

        # Check if target_domain in base target_domain
        if target_domain in FLASK_BASE_URLS:
            return api_response(400, "Can not remove base target domain")

        # Backup the target_domain
        backup_status, backup_message = backup_domain(target_domain)
        if not backup_status:
            warn(backup_message)

        # Remove the target_domain
        remove_status, remove_message = remove_domain(target_domain)
        if not remove_status:
            return api_response(400, remove_message)

        # Test and reload Nginx
        test_status, test_message = test_nginx()
        if not test_status:
            return api_response(400, test_message)
        
        reload_status, reload_message = reload_nginx()
        if not reload_status:
            return api_response(400, reload_message)

        return api_response(200, "Target domain removed successfully")

    except Exception as e:
        return api_response(400, f"Error: {str(e)}")

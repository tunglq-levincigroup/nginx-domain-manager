from services.file import exist_domain, write_domain, remove_domain, backup_domain
from services.nginx import test_nginx, reload_nginx
from services.certbot import register_certbot
from services.nettools import ping
from services.template import generate_nginx_conf
from utils.env import FLASK_BASE_URLS
from utils.response import api_response
from utils.logger import warn


def add_domain_controller(base_domain: str, domain: str):
    try:
        # Validate base domain
        if base_domain not in FLASK_BASE_URLS:
            return api_response(400, "Base domain not found.")

        # Check if domain is duplicate with domain
        if base_domain == domain:
            return api_response(400, "Can not add a same domain with base domain.")

        # Check if domain already exists
        if exist_domain(domain):
            return api_response(400, "Domain already exists.")

        # Ping the domain to ensure it's reachable
        ping_status, ping_message = ping(domain)
        if not ping_status:
            return api_response(400, ping_message)

        # Generate the Nginx configuration
        content = generate_nginx_conf(base_domain, domain)

        # Write the domain to the configuration
        write, write_message = write_domain(domain, content)
        if not write:
            return api_response(400, write_message)

        # Test and reload Nginx
        test_status, test_message = test_nginx()
        if not test_status:
            return api_response(400, test_message)
        
        reload_status, reload_message = reload_nginx()
        if not reload_status:
            return api_response(400, reload_message)

        # Register Certbot for the domain
        register_status, register_message = register_certbot(domain)
        if not register_status:
            return api_response(400, register_message)

        return api_response(200, "Domain added successfully")

    except Exception as e:
        return api_response(400, f"Error: {str(e)}")


def edit_domain_controller(base_domain: str, old_domain: str, domain: str):
    try:
        # Validate base domain
        if base_domain not in FLASK_BASE_URLS:
            return api_response(400, "Base domain not found.")

        # Check if domain is duplicate with domain
        if base_domain == domain:
            return api_response(400, "Can not edit a same domain with base domain.")
        
        # Check if old domain is duplicate with domain
        if old_domain == domain:
            return api_response(400, "Can not edit a same domain with old domain.")
        
        # Check if base domain is duplicate with old domain
        if base_domain == old_domain:
            return api_response(400, "Can not edit a same old domain with base domain.")

        # Check if the old domain exists
        if not exist_domain(old_domain):
            return api_response(400, "Old domain does not exist.")

        # Check if the new domain already exists
        if exist_domain(domain):
            return api_response(400, "New domain already exists.")

        # Ping the new domain to ensure it's reachable
        ping_status, ping_message = ping(domain)
        if not ping_status:
            return api_response(400, ping_message)

        # Generate the Nginx configuration
        content = generate_nginx_conf(base_domain, domain)

        # Write the new domain to the configuration
        write, write_message = write_domain(domain, content)
        if not write:
            return api_response(400, write_message)

        # Test and reload Nginx
        test_status, test_message = test_nginx()
        if not test_status:
            return api_response(400, test_message)
        
        reload_status, reload_message = reload_nginx()
        if not reload_status:
            return api_response(400, reload_message)

        # Register Certbot for the new domain
        register_status, register_message = register_certbot(domain)
        if not register_status:
            return api_response(400, register_message)

        # Backup and remove the old domain
        backup_status, backup_message = backup_domain(domain)
        if not backup_status:
            warn(backup_message)

        remove_status, remove_message = remove_domain(old_domain)
        if not remove_status:
            return api_response(400, remove_message)

        return api_response(200, "Domain edited successfully")

    except Exception as e:
        return api_response(400, f"Error: {str(e)}")


def remove_domain_controller(domain: str):
    try:
        # Check if the domain exists
        if not exist_domain(domain):
            return api_response(400, "Domain does not exist.")

        # Check if domain in base domain
        if domain in FLASK_BASE_URLS:
            return api_response(400, "Can not remove base domain")

        # Backup the domain
        backup_status, backup_message = backup_domain(domain)
        if not backup_status:
            warn(backup_message)

        # Remove the domain
        remove_status, remove_message = remove_domain(domain)
        if not remove_status:
            return api_response(400, remove_message)

        # Test and reload Nginx
        test_status, test_message = test_nginx()
        if not test_status:
            return api_response(400, test_message)
        
        reload_status, reload_message = reload_nginx()
        if not reload_status:
            return api_response(400, reload_message)

        return api_response(200, "Domain removed successfully")

    except Exception as e:
        return api_response(400, f"Error: {str(e)}")

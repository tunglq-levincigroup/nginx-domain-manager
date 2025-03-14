from services.file import exist_domain, write_domain, remove_domain
from services.nginx import test_nginx, reload_nginx
from services.certbot import generate_cert, exist_cert
from services.nettools import pings
from services.template import generate_nginx_ssl_conf_with_redirect
from utils.env import FLASK_BASE_URLS
from utils.response import api_response

def add_config_controller(base_domain: str, redirect_domain: str, target_domain: str):
    try:
        # Validate base domain
        if FLASK_BASE_URLS not in base_domain:
            return api_response(400, "Base domain not found.")

        # Check if given domains is duplicate
        if base_domain == redirect_domain:
            return api_response(400, "Base domain is duplicate with redirect domain")
        
        if base_domain == target_domain:
            return api_response(400, "Base domain is duplicate with target domain.")
        
        if base_domain == target_domain:
            return api_response(400, "Redirect domain is duplicate with target domain.")

        # Check if given domain already exists
        if exist_domain(redirect_domain):
            return api_response(400, "Redirect domain already exists.")
        
        if exist_domain(target_domain):
            return api_response(400, "Target domain already exists.")

        # Ping the domain to ensure it's reachable
        ping_status, ping_message = pings([base_domain, redirect_domain, target_domain])
        if not ping_status:
            return api_response(400, ping_message)

        # Certbot generate certificate
        if not exist_cert(target_domain):
            gen_status, gen_message = generate_cert(target_domain)
            if not gen_status:
                return api_response(400, gen_message)
        
        if not generate_cert(redirect_domain):
            gen_status, gen_message = generate_cert(redirect_domain)
            if not gen_status:
                return api_response(400, gen_message)

        # Generate the Nginx configuration
        content = generate_nginx_ssl_conf_with_redirect(base_domain, redirect_domain, target_domain)

        # Write the domain to the configuration
        write, write_message = write_domain(target_domain, content)
        if not write:
            return api_response(400, write_message)

        # Test and reload Nginx
        test_status, test_message = test_nginx()
        if not test_status:
            remove_domain(target_domain)
            return api_response(400, test_message)
        
        reload_status, reload_message = reload_nginx()
        if not reload_status:
            remove_domain(target_domain)
            return api_response(400, reload_message)

        return api_response(200, "Domain added successfully")

    except Exception as e:
        return api_response(400, f"Error: {str(e)}")

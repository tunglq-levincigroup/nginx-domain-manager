from services.file import *
from services.template import *
from services.nginx import *
from services.nettools import *

def add_domain_controller(domain: str):
    try:
        if exist_file(domain):
            return 'Cannot add an exist domain.', 400

        dns, dns_message = ping(domain)
        if not dns:
            return dns_message, 400

        content = generate_http(domain)
        write, write_message = write_file(domain, content)

        if not write:
            return write_message, 400

        register, register_message = register_certbot(domain)
        if not register:
            return register_message, 400

        return 'Domain added successfully.', 200
    except Exception as e:
        return f'Error while adding domain: {str(e)}', 400


def edit_domain_controller(old_domain: str, new_domain: str):
    try:
        if old_domain == new_domain:
            return 'Cannot update to the same domain.', 400

        dns, dns_message = ping(new_domain)
        if not dns:
            return dns_message, 400
        
        if exist_file(new_domain):
            return 'Cannot add an exist domain.', 400

        backup, backup_message = backup_file(old_domain)
        if not backup:
            print(backup_message)
            # no return

        remove, remove_message = delete_file(old_domain)
        if not remove:
            print(remove_message)
            # no return

        content = generate_http(new_domain)
        write, write_message = write_file(new_domain, content)
        if not write:
            return write_message, 400

        register, register_message = register_certbot(new_domain)
        if not register:
            return register_message, 400

        return 'Domain updated successfully.', 200
    except Exception as e:
        return f'Error while updating domain: {str(e)}', 400


def remove_domain_controller(domain: str):
    try:
        remove, remove_message = delete_file(domain)
        if not remove:
            return remove_message, 400

        return 'Domain removed successfully.', 200
    except Exception as e:
        return f'Error while removing domain: {str(e)}', 400

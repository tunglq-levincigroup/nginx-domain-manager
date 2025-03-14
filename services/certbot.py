import subprocess
from utils.env import FLASK_ADMIN_EMAIL
from utils.logger import info, error

######################### latest code
def exist_cert(domain: str):
    """
    Check if this certificate is exist in the system.

    Args:
        domain (str): The domain to check certitficates

    Returns:
        tuple[bool, str]: A tuple containing success status and a message.
    """
    try:
        result = subprocess.run(
            ["sudo", "certbot", "certificates"],
            capture_output=True,
            text=True,
            check=True
        )
        
        if domain in result.stdout:
            info(f"Certificate for {domain} exists.")
            return True
        else:
            info(f"No certificate found for {domain}.")
            return False

    except subprocess.CalledProcessError as e:
        error(f"Error checking certificate: {e}")
        return False

def generate_cert(domain: str):
    """
    Generate an SSL certificate for the given domain using Certbot and Nginx.

    Args:
        domain (str): The domain to generate the certificate for.

    Returns:
        tuple[bool, str]: A tuple containing success status and a message.
    """
    command = [
        "sudo", "certbot", "certonly", 
        "--nginx", "-d", domain,
        "--non-interactive", "--agree-tos",
        "--email", FLASK_ADMIN_EMAIL, "--redirect"
    ]

    info(f"Executing Certbot command: {' '.join(command)}")

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        info(result.stdout)
        return True, "Certificate generated successful"
    except subprocess.CalledProcessError as e:
        error(e.stderr)
        return False, e.stderr
    except Exception as e:
        error(f"Unexpected error: {str(e)}")
        return False, "Certificate registration failed due to an unexpected error"
    
def delete_cert(domain: str):
    """
    Delete certbot ssl certificate from system.

    Args:
        domain (str): The domain to delete the certificate for.

    Returns:
        tuple[bool, str]: A tuple containing success status and a message.
    """
    command = [
        "sudo", "certbot", "delete", 
        "--cert-name", domain,
        "--non-interactive", "--agree-tos",
        "--email", FLASK_ADMIN_EMAIL, "--redirect"
    ]

    info(f"Executing Certbot command: {' '.join(command)}")

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        info(result.stdout)
        return True, "Certificate deleted successful"
    except subprocess.CalledProcessError as e:
        error(e.stderr)
        return False, e.stderr
    except Exception as e:
        error(f"Unexpected error: {str(e)}")
        return False, "Certificate registration failed due to an unexpected error"


##################### this function is not up to date
##################### install http -> then generate cert and install automatically
def register_certbot(domain: str) -> tuple[bool, str]:
    """
    Registers an SSL certificate for the given domain using Certbot and Nginx.

    Args:
        domain (str): The domain to register the certificate for.

    Returns:
        tuple[bool, str]: A tuple containing success status and a message.
    """
    command = [
        "sudo", "certbot", "--nginx", "-d", domain,
        "--non-interactive", "--agree-tos",
        "--email", FLASK_ADMIN_EMAIL, "--redirect"
    ]

    info(f"Executing Certbot command: {' '.join(command)}")

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        info(result.stdout)
        return True, "Certificate registration successful"
    except subprocess.CalledProcessError as e:
        error(e.stderr)
        return False, e.stderr
    except Exception as e:
        error(f"Unexpected error: {str(e)}")
        return False, "Certificate registration failed due to an unexpected error"
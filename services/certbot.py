import subprocess
from utils.env import FLASK_ADMIN_EMAIL
from utils.logger import info, error

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

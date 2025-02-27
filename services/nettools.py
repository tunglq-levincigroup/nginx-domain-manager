import socket
from utils.env import FLASK_SERVER_IP
from utils.logger import info, error

def ping(domain: str) -> tuple[bool, str]:
    """
    Resolves the IP address of a domain and checks if it matches the server IP.

    Args:
        domain (str): The domain name to resolve.

    Returns:
        tuple[bool, str]: Success status and a message.
    """
    try:
        domain_ip = socket.gethostbyname(domain)
        info(f"Resolved IP for {domain}: {domain_ip}")

        if domain_ip == FLASK_SERVER_IP:
            return True, f"IP matches FLASK_SERVER_IP: {domain_ip}"
        else:
            return False, f"IP mismatch. Domain IP: {domain_ip}, Expected: {FLASK_SERVER_IP}"

    except socket.gaierror as e:
        error(f"Failed to resolve domain {domain}: {e}")
        return False, f"Failed to resolve domain {domain}"

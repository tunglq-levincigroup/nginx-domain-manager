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
            return False, f"IP mismatch for domain {domain}"

    except socket.gaierror as e:
        error(f"Failed to resolve domain {domain}: {e}")
        return False, f"Failed to resolve domain {domain}"


def pings(domains: list[str]):
    """
    Resolves the IP address of a domain and checks if it matches the server IP.

    Args:
        domains (list[str]): The list of domain name to resolve.

    Returns:
        tuple[bool, str]: Success status and a message.
    """
    try:
        logs = []
        for domain in domains:
            ping_success, message = ping(domain)
            if not ping_success:
                logs.append(f"{domain}: {message}")

        if logs:
            logs_message = '\n'.join(logs)
            error(logs_message)
            return False, f"DNS check failed:\n{logs_message}"

        response_message = "All DNS records are correct."
        info(response_message)
        return True, response_message
    except Exception as e:
        error(f"Failed to resolve domains {domains}: {e}")
        return False, f"Failed to resolve domains: {domains}"
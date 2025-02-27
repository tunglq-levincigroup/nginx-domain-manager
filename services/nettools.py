import socket
from utils.env import FLASK_SERVER_IP

def ping(domain: str):
    try:
        # Get the IP address of the domain
        domain_ip = socket.gethostbyname(domain)
        
        # Check if the IP matches the FLASK_SERVER_IP
        if domain_ip == FLASK_SERVER_IP:
            return True, f"IP matches FLASK_SERVER_IP: {domain_ip}"
        else:
            return False, f"IP does not match. Domain IP: {domain_ip}, FLASK_SERVER_IP: {FLASK_SERVER_IP}"
    
    except socket.gaierror:
        return False, "Failed to resolve domain"

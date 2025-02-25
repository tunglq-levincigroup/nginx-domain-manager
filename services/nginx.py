import subprocess
from services.env import FLASK_ADMIN_EMAIL

def reload_nginx():
    result = subprocess.run(["sudo", "/usr/sbin/nginx", "-s", "reload"], capture_output=True, text=True)
    if result.returncode != 0:
        return False, result.stderr
    return True, result.stdout # success

def test_nginx():
    result = subprocess.run(["sudo", "/usr/sbin/nginx", "-t"], capture_output=True, text=True)
    if result.returncode != 0:
        return False, result.stderr
    return True, result.stdout # success

def register_certbot(domain: str):
    result = subprocess.run(["sudo", "certbot", "--nginx", "-d", domain, '--non-interactive', '--agree-tos', '--email', FLASK_ADMIN_EMAIL, '--redirect'], capture_output=True, text=True)
    if result.returncode != 0:
        return False, result.stderr
    return True, result.stdout # success
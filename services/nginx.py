import subprocess
from services.env import FLASK_ADMIN_EMAIL

def reload_nginx():
    try:
        result = subprocess.run(["sudo", "/usr/sbin/nginx", "-s", "reload"], capture_output=True, text=True)
        if result.returncode != 0:
            return False, result.stderr
        return True, result.stdout # success
    except Exception as e:
        return False, str(e)

def test_nginx():
    try:
        result = subprocess.run(["sudo", "/usr/sbin/nginx", "-t"], capture_output=True, text=True)
        if result.returncode != 0:
            return False, result.stderr
        return True, result.stdout # success
    except Exception as e:
        return False, str(e)

def register_certbot(domain: str):
    try:
        command = [
            "sudo", "certbot", "--nginx", "-d", domain,
            '--non-interactive', '--agree-tos',
            '--email', FLASK_ADMIN_EMAIL, '--redirect'
        ]
        print(f"Running command: {' '.join(command)}")

        result = subprocess.run(command, capture_output=True, text=True)

        print("Certbot output:", result.stdout)
        print("Certbot errors:", result.stderr)

        if result.returncode != 0:
            return False, result.stderr
        return True, result.stdout  # success
    except Exception as e:
        return False, str(e)
import subprocess
from utils.env import FLASK_ADMIN_EMAIL

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
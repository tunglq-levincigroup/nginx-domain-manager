import subprocess
from utils.env import FLASK_ACME

def generate_txt_record(domain: str) -> tuple[bool, str, dict | None]:
    try:
        command = [
            FLASK_ACME, "--issue", 
            "-d", domain, 
            "--dns", "--yes-I-know-dns-manual-mode-enough-go-ahead-please",
            "--test"
        ]

        print(f"Running command: {' '.join(command)}")

        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode == 3:
            lines = result.stdout.splitlines()
            name = None
            value = None

            for line in lines:
                if 'Domain:' in line:
                    name = line.split("Domain: '")[1].split("'")[0]
                if 'TXT value:' in line:
                    value = line.split("TXT value: '")[1].split("'")[0]

            if name and value:
                return True, "Success", {"name": name, "value": value}

        return False, "Failed to retrieve TXT record", None
    except Exception as e:
        return False, str(e), None

def apply_txt_record(domain: str):
    try:
        command = [
            FLASK_ACME, "--issue", 
            "-d", domain, 
            "--dns", "--yes-I-know-dns-manual-mode-enough-go-ahead-please",
            "--renew",
            "--test"
        ]

        print(f"Running command: {' '.join(command)}")

        result = subprocess.run(command, capture_output=True, text=True)
        print(result.returncode)
        print(result.stdout)
        return True, "test"
    except Exception as e:
        return False, str(e), None
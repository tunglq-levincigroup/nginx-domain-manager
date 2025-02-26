import subprocess
import re
import time
from services.env import *

def register_ssl(domain: str):
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
    
store = {}

def generate_txt_record(domain: str) -> tuple[bool, str, dict | None]:
    try:
        command = [
            "sudo", "certbot", "certonly", "--manual", 
            "--preferred-challenges", "dns", 
            "-d", domain, 
            "--manual-public-ip-logging-ok",
            "--dry-run", 
        ]

        print(f"Running command: {' '.join(command)}")

        # Khởi chạy lệnh Certbot
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        data = []
        # Đọc output từng dòng để tránh blocking
        for line in process.stdout:
            data.append(line.strip())
            if len(data) > 9:
                break
        store[domain] = process.pid

        return True, "TXT record generated successfully", {"name": data[5], "value": data[9]}
    except Exception as e:
        process.terminate()
        return False, str(e), {}

def continue_txt_record(domain: str):
    if domain not in store:
        return False, f"No ongoing certbot process for domain {domain}"

    try:
        process = store[domain]
        process.stdin.write('\n')  # Gửi Enter để tiếp tục
        process.stdin.flush()
        process.wait()  # Đợi Certbot kết thúc

        del store[domain]  # Xoá tiến trình khỏi store
        return True, "Certbot validation completed"

    except Exception as e:
        return False, str(e)
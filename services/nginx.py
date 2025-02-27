import subprocess

def reload_nginx():
    try:
        command = ["sudo", "/usr/sbin/nginx", "-s", "reload"]
        print(f"Running command: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            return False, result.stderr
        return True, result.stdout # success
    except Exception as e:
        return False, str(e)

def test_nginx():
    try:
        command = ["sudo", "/usr/sbin/nginx", "-t"]
        print(f"Running command: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            return False, result.stderr
        return True, result.stdout # success
    except Exception as e:
        return False, str(e)
import subprocess
from utils.logger import info, error

def run_nginx_command(command: list[str]) -> tuple[bool, str]:
    """
    Runs an Nginx-related shell command and captures its output.

    Args:
        command (list[str]): The command to execute.

    Returns:
        tuple[bool, str]: Success status and command output or error message.
    """
    try:
        info(f"Executing command: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            error(result.stderr)
            return False, result.stderr

        info(result.stdout)
        return True, result.stdout
    except Exception as e:
        error(f"Command execution failed: {str(e)}")
        return False, str(e)

def reload_nginx() -> tuple[bool, str]:
    """Reloads the Nginx service."""
    return run_nginx_command(["sudo", "/usr/sbin/nginx", "-s", "reload"])

def test_nginx() -> tuple[bool, str]:
    """Tests the Nginx configuration for syntax errors."""
    return run_nginx_command(["sudo", "/usr/sbin/nginx", "-t"])

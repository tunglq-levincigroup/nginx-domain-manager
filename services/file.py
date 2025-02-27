import os
import shutil
from datetime import datetime
from utils.env import FLASK_CONFIG_PATH, FLASK_BACKUP
from utils.logger import info, error

DIR = FLASK_CONFIG_PATH
BACKUP_DIR = FLASK_BACKUP

def ensure_directory_exists(directory: str) -> None:
    """Ensures the given directory exists, creating it if necessary."""
    try:
        os.makedirs(directory, exist_ok=True)
        info(f"Create directory: {directory}")
    except OSError as e:
        error(f"Failed to create directory {directory}: {e}")

def write_domain(domain: str, content: str) -> tuple[bool, str]:
    """
    Writes the specified content to a domain configuration file.

    Args:
        domain (str): The domain name (used for directory and filename).
        content (str): The content to write into the configuration file.

    Returns:
        tuple[bool, str]: Success status and a message.
    """
    domain_dir = os.path.join(DIR, domain)
    ensure_directory_exists(domain_dir)
    filename = os.path.join(domain_dir, f"{domain}.conf")

    try:
        with open(filename, 'w') as file:
            file.write(content)
        info(f"Content written to {filename}")
        return True, f"Content written to {filename}"
    except Exception as e:
        error(f"Error writing to file {filename}: {e}")
        return False, f"Error writing to file: {e}"


def remove_domain(domain: str) -> tuple[bool, str]:
    """
    Deletes the domain configuration file and its directory if empty.

    Args:
        domain (str): The domain name (used for directory and filename).

    Returns:
        tuple[bool, str]: Success status and a message.
    """
    dirname = os.path.join(DIR, domain)
    filename = os.path.join(dirname, f"{domain}.conf")

    try:
        if not os.path.exists(filename):
            return False, f"File {filename} does not exist."

        os.remove(filename)
        info(f"File {filename} deleted")

        if os.path.exists(dirname) and not os.listdir(dirname):
            os.rmdir(dirname)
            info(f"Directory {dirname} deleted")

        return True, f"File {filename} and directory {dirname} deleted successfully."
    except Exception as e:
        error(f"Error deleting file or directory: {e}")
        return False, f"Error deleting file or directory: {e}"


def backup_domain(domain: str) -> tuple[bool, str]:
    """
    Creates a timestamped backup of the domain configuration file.

    Args:
        domain (str): The domain name (used for directory and filename).

    Returns:
        tuple[bool, str]: Success status and a message.
    """
    old_filename = os.path.join(DIR, domain, f"{domain}.conf")

    if not os.path.exists(old_filename):
        return False, f"Source file {old_filename} does not exist."

    backup_dir = os.path.join(BACKUP_DIR, domain)
    ensure_directory_exists(backup_dir)

    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    backup_filename = os.path.join(backup_dir, f"{timestamp}-{domain}.conf")

    try:
        shutil.copy2(old_filename, backup_filename)
        info(f"Backup created at {backup_filename}")
        return True, f"Backup created at {backup_filename}"
    except Exception as e:
        error(f"Error backing up file {old_filename} to {backup_filename}: {e}")
        return False, f"Error backing up file: {e}"


def exist_domain(domain: str) -> bool:
    """Checks if the domain configuration file exists."""
    filename = os.path.join(DIR, domain, f"{domain}.conf")
    return os.path.exists(filename)
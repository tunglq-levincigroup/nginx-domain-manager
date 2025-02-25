import os
import shutil
from datetime import datetime

DIR = 'conf.d'
BACKUP_DIR = 'backup'

def ensure_directory_exists(directory: str):
    """Creates the directory if it does not exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def write_file(domain: str, content: str) -> tuple[bool, str]:
    """
    Writes the specified content to a file.
    
    :param domain: Path to the file where content will be written.
    :param content: The content to write to the file.
    """
    domain_dir = f'{DIR}/{domain}'
    ensure_directory_exists(domain_dir)
    filename = f'{domain_dir}/{domain}.conf'
    try:
        with open(filename, 'w') as file:
            file.write(content)
    except Exception as e:
        return False, f"Error writing to file: {e}"
    return True, f"Content written to {filename}"

def delete_file(domain: str) -> tuple[bool, str]:
    """
    Deletes the specified file.
    
    :param domain: Path to the file that needs to be deleted.
    """
    filename = f'{DIR}/{domain}/{domain}.conf'
    try:
        if not os.path.exists(filename):
            return False, f"File {filename} does not exist."
        os.remove(filename)
    except Exception as e:
        return False, f"Error deleting file: {e}"
    return True, f"File {filename} deleted successfully."

def backup_file(domain):
    """
    Backs up the specified file by copying it to a backup directory.
    
    :param domain: Path to the source file to be backed up.
    """
    old_filename = f'{DIR}/{domain}/{domain}.conf'
    if not os.path.exists(old_filename):
        return False, f"Source file {old_filename} does not exist."

    backup_dir = f'{BACKUP_DIR}/{domain}'
    ensure_directory_exists(backup_dir)

    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    filename = f'{backup_dir}/{timestamp}-{domain}.conf'
    try:
        shutil.copy2(old_filename, filename)
    except Exception as e:
        return False, f"Error backing up file: {e}"
    return True, f"Backup created at {filename}"

def exist_file(domain: str):
    filename = f'{DIR}/{domain}/{domain}.conf'
    return os.path.exists(filename)
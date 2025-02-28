import os

def get_env_variable(name: str, default: str = None):
    """Helper function to retrieve environment variables with optional default values."""
    value = os.getenv(name, default)
    if value is None:
        raise ValueError(f"Environment variable '{name}' is required but not set.")
    return value

# Retrieve environment variables with proper error handling
FLASK_SERVER_IP = get_env_variable("FLASK_SERVER_IP", "127.0.0.1")
FLASK_ADMIN_EMAIL = get_env_variable("FLASK_ADMIN_EMAIL", "admin@admin.com")
FLASK_BACKUP = get_env_variable("FLASK_BACKUP", "./backups")
FLASK_CONFIG_PATH = get_env_variable("FLASK_CONFIG_PATH", "./conf.d")
FLASK_BASE_URLS = get_env_variable("FLASK_BASE_URLS", "")
from datetime import datetime

def log(level: str, message: str) -> None:
    """
    Logs a message with a specified severity level and a UTC timestamp.

    Args:
        level (str): The log level (INFO, WARN, ERROR).
        message (str): The message to log.
    """
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] - [{level}] - {message}")

def info(message: str) -> None:
    """Logs an info-level message."""
    log("INFO", message)

def warn(message: str) -> None:
    """Logs a warning-level message."""
    log("WARN", message)

def error(message: str) -> None:
    """Logs an error-level message."""
    log("ERROR", message)
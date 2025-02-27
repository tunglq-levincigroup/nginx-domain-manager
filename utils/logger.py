from datetime import datetime

def info(message: str):
    now = datetime.utcnow()
    print(f'[{now.strftime("%Y-%m-%d %H:%M:%S")}] - [INFO] - {message}')

def warn(message: str):
    now = datetime.utcnow()
    print(f'[{now.strftime("%Y-%m-%d %H:%M:%S")}] - [WARN] - {message}')

def error(message: str):
    now = datetime.utcnow()
    print(f'[{now.strftime("%Y-%m-%d %H:%M:%S")}] - [ERROR] - {message}')

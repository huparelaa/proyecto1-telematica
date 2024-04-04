import socket
import os

def get_my_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
    except Exception as e:
        print(f"Error obtaining IP address: {e}")
        ip = None # Fallback to localhost
    return ip

def list_dir(path):
    return os.listdir(path) 

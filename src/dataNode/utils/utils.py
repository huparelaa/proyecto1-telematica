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
 

def get_files_info():
    base_dir = "./files"
    parts_routes = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            if "-_-" in file:
                # Remove '.files/' from the path
                path = os.path.join(root, file)[8:]
                parts_routes.append(path)
    return parts_routes

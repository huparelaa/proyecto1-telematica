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

def get_files_routes():
    base_directory = "./files"
    parts_routes = []
    for root, _, files in os.walk(base_directory):
        for file in files:
            if "-_-" in file:  # Identifies the file parts
                complete_route = os.path.join(root, file)
                parts_routes.append(complete_route)
    return parts_routes
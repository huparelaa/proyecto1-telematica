import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()

name_node_ip = os.getenv("NAMENODE_IP")
name_node_port = os.getenv("NAMENODE_PORT")


def get_datanode_address(file_name, file_path, block_num):
    data = {
        "file_name": file_name,
        "file_path": file_path,
        "block_num": block_num
     } 
    try: 
        response = requests.post(f"http://{name_node_ip}:{name_node_port}/namenode/api/v1/datanode_write_list/", json=data)
        response.raise_for_status()
        json_response = response.json()
        if "dataNodesAvailable" in json_response:
            return json_response["dataNodesAvailable"]
        else:
            return None
    except requests.exceptions.RequestException as e:
        print("No such file or directory")
        return None
    
def get_datanode_address_read(file_name, file_path):
    
    route = f"{file_path}{file_name}/{file_name}"
    # remove first '/'
    if route[0] == "/":
        route = route[1:]
    try: 
        response = requests.get(f"http://{name_node_ip}:{name_node_port}/namenode/api/v1/datanode_read_list/?route={route}")
        response.raise_for_status()
        json_response = response.json()
        if "dataNodes" in json_response:
            return json_response["dataNodes"]
        else:
            return None
    except requests.exceptions.RequestException as e:
        return None

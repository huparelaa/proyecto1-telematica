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
        print(json.dumps(response.json(), indent=4))
    except requests.exceptions.RequestException as e:
        print("No such file or directory")
        return None
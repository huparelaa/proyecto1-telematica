from utils.utils import get_my_ip, get_files_info
from dotenv import load_dotenv
import requests
import os
from utils.utils import get_my_ip, get_files_info
from utils.heartbeat import sendFileToDataNode
import sys
import json
import time
import threading

load_dotenv()

HEARTBEAT_INTERVAL = 5
HEARTBEAT_URL_PATH = "/api/v1/heartbeat"
nameNode_ip = os.getenv("NAMENODE_IP")
nameNode_port = os.getenv("NAMENODE_PORT")

data_node_status = "active"

def heartBeat(scheduler):
    scheduler.enter(HEARTBEAT_INTERVAL, 1, heartBeat, (scheduler,))
    data = {
        "ip_address": get_my_ip(),
        "port": str(os.environ.get('PORT', 50051)),
        "block_list": get_files_info(),
        "status": data_node_status
    }

    print(data)
    nameNode_endpoint = f"http://{nameNode_ip}:{nameNode_port}/namenode/api/v1/heartbeat/"
    try:
        response = requests.post(nameNode_endpoint, json=data)
        response.raise_for_status()  # Esto lanzará un error si la solicitud falla
        threading.Thread(target=manageHeartbeatResponse, args=(response.json(),), daemon=True).start()

        return response.json()  # Retorna la respuesta del NameNode
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
        sys.exit(1)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
        sys.exit(1)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)
        sys.exit(1)

def manageHeartbeatResponse(response):
        global data_node_status
        data_node_status = "busy"
        print(json.dumps(response, indent=4))
        if response["command"] == "replicate":
            for data_node in response["data"]:
                file_path = data_node["file_path"]
                data_node_address = data_node["data_node_address"]
                sendFileToDataNode(file_path, data_node_address)
            print("File replicated")
        if response["command"] == "delete":
            file_path = response["file_path"]
            os.remove(f"./files/{file_path}")
            print("File deleted")
        data_node_status = "active"

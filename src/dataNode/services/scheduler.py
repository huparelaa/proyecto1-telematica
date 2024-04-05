import requests
import os
from utils.utils import get_my_ip
from utils.heartbeat import manageHeartbeatResponse
import sys
from dotenv import load_dotenv
load_dotenv()

HEARTBEAT_INTERVAL = 5
HEARTBEAT_URL_PATH = "/api/v1/heartbeat"
nameNode_ip = os.getenv("NAMENODE_IP")
nameNode_port = os.getenv("NAMENODE_PORT")

def heartBeat(scheduler):
    scheduler.enter(HEARTBEAT_INTERVAL, 1, heartBeat, (scheduler,))

    data = {
        "ip_address": get_my_ip(),
        "port": os.getenv("GRPC_PORT"),
        "block_list": getFilesInfo(),
        "status": "active"
    }

    nameNode_endpoint = f"http://{nameNode_ip}:{nameNode_port}/namenode/api/v1/heartbeat/"
    try:
        # Realizar la solicitud POST
        response = requests.post(nameNode_endpoint, json=data)
        response.raise_for_status()  # Esto lanzará un error si la solicitud falla
        manageHeartbeatResponse(response.json())
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
    return "Could not perform the hearBeat operation."

def getFilesInfo():
    base_dir = "./files"
    parts_routes = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            if "-_-" in file:
                # Remove '.files/' from the path
                path = os.path.join(root, file)[7:]
                parts_routes.append(path)
    return parts_routes

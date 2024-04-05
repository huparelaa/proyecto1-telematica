from utils.utils import get_my_ip, get_files_info
from dotenv import load_dotenv
import requests
import os
from utils.utils import get_my_ip, get_files_info
from utils.heartbeat import manageHeartbeatResponse
import sys

load_dotenv()

HEARTBEAT_INTERVAL = 5
HEARTBEAT_URL_PATH = "/api/v1/heartbeat"
nameNode_ip = os.getenv("NAMENODE_IP")
nameNode_port = os.getenv("NAMENODE_PORT")

def heartBeat(scheduler):
    scheduler.enter(HEARTBEAT_INTERVAL, 1, heartBeat, (scheduler,))
    data = {
        "ip_address": get_my_ip(),
        "port": str(os.environ.get('PORT', 50051)),
        "available_space": 1000,
        "block_list": get_files_info(),
    }

    print(data)
    nameNode_endpoint = f"http://{nameNode_ip}:{nameNode_port}/namenode/api/v1/heartbeat/"
    try:
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

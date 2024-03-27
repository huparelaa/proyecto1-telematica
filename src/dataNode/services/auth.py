import sys
from utils.utils import get_my_ip
import requests
from dotenv import load_dotenv
import os

load_dotenv()

def login():
    my_ip = get_my_ip()
    my_grpc_port = os.getenv("GRPC_PORT")
    heartbeat_port = os.getenv("HEARTBEAT_PORT")
    nameNode_ip = os.getenv("NAMENODE_IP")
    nameNode_port = os.getenv("NAMENODE_PORT")

    if my_ip is not None:
        # Construir la URL del endpoint del NameNode
        nameNode_endpoint = f"http://{nameNode_ip}:{nameNode_port}/api/v1/login"

        # Datos para enviar en el body del POST request
        data = {"ip": my_ip, "grpcPort": my_grpc_port, "heartbeatPort": heartbeat_port}

        try:
            # Realizar la solicitud POST
            response = requests.post(nameNode_endpoint, json=data)
            response.raise_for_status()  # Esto lanzará un error si la solicitud falla
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

    return "Could not perform the login operation."
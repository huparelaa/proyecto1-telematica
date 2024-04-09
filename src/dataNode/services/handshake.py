import sys
from utils.utils import get_my_ip
import requests
from dotenv import load_dotenv
import os
from utils.utils import get_files_info

load_dotenv()

def handShake():
    my_ip = get_my_ip()
    PORT = int(os.environ.get('PORT', 50051))     
    nameNode_ip = os.getenv("NAMENODE_IP")
    nameNode_port = os.getenv("NAMENODE_PORT")

    if my_ip is not None:
        # Construir la URL del endpoint del NameNode
        nameNode_endpoint = f"http://{nameNode_ip}:{nameNode_port}/namenode/api/v1/handshake/"

        # Datos para enviar en el body del POST request
        data = {
            "ip_address": my_ip, 
            "port": str(PORT), 
            "block_list":  get_files_info() 
        }

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

    return "Could not perform the handShake operation."
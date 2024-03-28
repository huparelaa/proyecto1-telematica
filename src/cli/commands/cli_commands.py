import os
from dotenv import load_dotenv
import requests

load_dotenv()

def namenode_address():
    name_node_ip = os.getenv("NAMENODE_IP")
    name_node_port = os.getenv("NAMENODE_PORT")

    return f"http://{name_node_ip}:{name_node_port}/namenode/api/v1"

def ls(my_route):
    try:
        #remove last "/"
        if my_route[-1] == "/":
            my_route = my_route[:-1]
        
        my_route = my_route.replace("/", "%2F")
        response = requests.get(f"{namenode_address()}/ls?route={my_route}")
        response.raise_for_status()
        data=response.json()['directory_content']
        for file in data:
            print(file)
    except requests.exceptions.RequestException as e:
        print("No such file or directory")

def cd(my_route, directory):
    if directory == "..":
        return "/".join(my_route.split("/")[:-2]) + "/"
    else:
        error_message = "No such file or directory:"
        new_route = f"{my_route}{directory}"
        try:
            response = requests.post(f"{namenode_address()}/cd", json={"route": new_route})
            response.raise_for_status()
            # if begins with error_message
            if response.json()["message"].startswith(error_message):
                print(response.json()["message"])
                return my_route
            return new_route+"/"
        except requests.exceptions.RequestException as e:
            print("No such file or directory")
            return my_route
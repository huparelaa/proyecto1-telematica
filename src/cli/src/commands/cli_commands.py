import os
from dotenv import load_dotenv
import requests
from utils.filemanager import split_file, join_files
from connection.nameNodeConn import get_datanode_address
from connection.dataNodeConn import send_files_to_datanode, download_files_from_datanode

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

def cd(my_route, directory, username):
    if directory == "..":
        if my_route == f"/{username}/":
            return my_route
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
        
def mkdir(my_route, directory):
    try:
        response = requests.post(f"{namenode_address()}/mkdir", json={"route": f"{my_route}{directory}"})
        response.raise_for_status()
        print("Directory created")
    except requests.exceptions.RequestException as e:
        print("No such file or directory")

def write(my_route, file_name):
    try:
        split_file(f"../uploads/{file_name}")
        route = f"{my_route}{file_name}/"
        send_files_to_datanode(route=route, data_node_address=get_datanode_address())
        print(f"File {file_name} written")
        
    except FileNotFoundError:
        return
    
def read(my_route, file_name):
    try:
        download_files_from_datanode(data_node_address=get_datanode_address(), file_name=file_name, file_path=my_route)
        join_files(file_name)
        print(f"File {file_name} read, check the downloads folder")
    except FileNotFoundError:
        print("File not found")
        return
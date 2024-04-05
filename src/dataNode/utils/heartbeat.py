from filetransfer.replication import uploadFileWithGrpc
def manageHeartbeatResponse(response):
    if response["command"] == "replicate":
        data_node_ip = response["data_node_ip"]
        data_node_port = response["data_node_port"]
        file_path = response["file_path"]
        sendFileToDataNode(file_path, data_node_ip, data_node_port)
        print("File replicated")

def sendFileToDataNode(file_path, dataNode_ip, dataNode_port):
    try:
        print(f"./files{file_path}")
        with open(f"./files{file_path}", "rb") as file:
            file_content = file.read()
            response = uploadFileWithGrpc(file_path, file_content, f"{dataNode_ip}:{dataNode_port}")
            if response:
                print("File sent successfully")
            else:
                print("File not sent")
    except Exception as e:
        print(e)
        print("Error sending file")
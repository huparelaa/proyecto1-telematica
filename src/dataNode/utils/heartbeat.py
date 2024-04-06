from filetransfer.replication import uploadFileWithGrpc
def manageHeartbeatResponse(response):

    if response["command"] == "replicate":
        for data_node in response["data"]:
            file_path = data_node["file_path"]
            data_node_address = data_node["data_node_address"]
            sendFileToDataNode(file_path, data_node_address)
        print("File replicated")

def sendFileToDataNode(file_path, data_node_address):
    try:
        print(f"./files/{file_path}")
        with open(f"./files/{file_path}", "rb") as file:
            file_content = file.read()
            response = uploadFileWithGrpc(file_path, file_content, data_node_address)
            if response:
                print("File sent successfully")
            else:
                print("File not sent")
    except Exception as e:
        print(e)
        print("Error sending file")
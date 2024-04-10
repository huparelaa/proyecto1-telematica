from NameNode import NameNode
from fastapi import FastAPI, HTTPException
from schemas import *
import json

app = FastAPI()
nameNode = NameNode()
nameNode.start_heartbeat_checker()

def log_action(action, route):
    with open("editlog.txt", "a") as file:
        file.write(f"{action}: {route}\n")

# Routes for the data nodes

@app.post("/namenode/api/v1/handshake/")
async def dataNodeHandshake(request: HandShakeRequest):
    success = nameNode.createDataNode(request)
    if success: 
        nameNode.updateBlockMap(request.ip_address, request.port, request.block_list)
        return { "message": "HandShake datanode succesfully!", "success": success }
    else: 
        return HTTPException(status_code=404, detail="DataNode already exists")
    
@app.post("/namenode/api/v1/heartbeat/")
async def dataNodeHeartbeat(request: HeartbeatRequest):
        print("HeartBeat", json.dumps(request.status, indent=4))
        success, command, blocks_to_replicate = nameNode.heartBeat(request)
        if success: 
            return { "message": "HeartBeat datanode succesfully!", "success": success, "command": command, "data": blocks_to_replicate }
        else:
            return HTTPException(status_code=404, detail="DataNode does not exist")
    
# Routes to read and write files

@app.get("/namenode/api/v1/datanode_read_list/")
async def getReadFileDataNodes(route: str):
    datanodes = nameNode.getReadDataNodes(route)
    return { "dataNodes": datanodes }

@app.post("/namenode/api/v1/datanode_write_list/")
async def selectWriteFileDataNodes(request: FileWriteRequest):
    #check if the file already exists
    blockMap = nameNode.blockMap
    # delete first '/'
    if request.file_path[0] == "/":
        request.file_path = request.file_path[1:]

    if f"{request.file_path}{request.file_name}/{request.file_name}" in blockMap:
        raise HTTPException(status_code=400, detail="File already exists")

    dataNodeWriteList = nameNode.getWriteDataNodes(request)
    return { "dataNodesAvailable": dataNodeWriteList }

@app.post("/namenode/api/v1/confirm_write/")
async def confirmWrite(request: RouteRequest):
    success = nameNode.directoryTree.add_files(request)
    if success: 
        log_action("write", request.route)
        return { "message": "File successfully written!", "success": success }
    else: 
        HTTPException(status_code=404, detail="No such file or directory")
# Routes for the directory tree

@app.get("/namenode/api/v1/ls/")
async def listDirectory(route: str):
    directory_content = nameNode.directoryTree.ls(route)
    return { "directory_content": directory_content }

@app.post("/namenode/api/v1/mkdir/")
async def makeDirectory(route: RouteRequest):
    success = nameNode.directoryTree.add_directory(route.route)
    if success: 
        log_action("mkdir", route.route)
        return { "message": "Directory successfully created!", "success": success }
    else: 
        return { "message": "Directory failed created!", "success": success }

@app.post("/namenode/api/v1/cd/")
async def changeDirectory(request: RouteRequest):
    targetRequest = nameNode.directoryTree.get_directory(request.route)
    if targetRequest: 
        return { "message": "Change Directory!", "route": request.route }
    else: 
        raise HTTPException(status_code=404, detail="No such file or directory")

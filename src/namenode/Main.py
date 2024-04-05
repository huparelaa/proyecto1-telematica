from NameNode import NameNode
from fastapi import FastAPI, HTTPException
from schemas import *

app = FastAPI()
nameNode = NameNode()
nameNode.start_heartbeat_checker()

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
    print(request.ip_address, request.port)
    success = nameNode.heartBeat(request)
    if success: 
        return { "message": "HeartBeat datanode succesfully!", "success": success }
    else:
        return HTTPException(status_code=404, detail="DataNode does not exist")
    
@app.get("/namenode/api/v1/datanode_read_list/")
async def getReadFileDataNodes(route: str):
    print(route)
    datanodes = nameNode.getReadDataNodes(route)
    return { "dataNodes": datanodes }

@app.post("/namenode/api/v1/datanode_write_list/")
async def selectWriteFileDataNodes(request: FileWriteRequest):
    dataNodeWriteList = nameNode.getWriteDataNodes("", 3, 3, "")
    return { "dataNodesAvailable": dataNodeWriteList }

@app.get("/namenode/api/v1/ls/")
async def listDirectory(route: str):
    directory_content = nameNode.directoryTree.ls(route)
    return { "directory_content": directory_content }

@app.post("/namenode/api/v1/mkdir/")
async def makeDirectory(route: RouteRequest):
    success = nameNode.directoryTree.add_directory(route.route)
    if success: 
        return { "message": "Directory successfully created!", "success": success }
    else: 
        return { "message": "Directory failed created!", "success": success }

@app.post("/namenode/api/v1/cd/")
async def changeDirectory(request: RouteRequest):
    targetRequest = nameNode.directoryTree.get_directory(request.route)
    if targetRequest: 
        return { "message": "Change Directory!", "route": request.route }
    else: 
        return HTTPException(status_code=404, detail="No such file or directory")

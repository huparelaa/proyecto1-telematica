from NameNode import NameNode
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
app = FastAPI()
nameNode = NameNode()

nameNode.directoryTree.add_directory("/txt")
nameNode.directoryTree.add_files("/txt/hola.mp3", "", "")
nameNode.directoryTree.add_files("/txt/hola1.mp3", "", "")
nameNode.directoryTree.add_files("/txt/hola2.mp3", "", "")
nameNode.directoryTree.add_directory("/txt/hola")
nameNode.directoryTree.add_files("/txt/hola/clo.mp4", "", "")
nameNode.directoryTree.add_files("/txt/hola/ro.mp3", "", "")
nameNode.directoryTree.add_files("/txt/hola/cl.mp3", "", "")
nameNode.directoryTree.add_directory("/txt1")
nameNode.directoryTree.add_directory("/txt2")

class HandShakeRequest(BaseModel):
    ip_address: str
    port: str

class HeartbeatRequest(BaseModel):
    ip_address: str
    port: str
    block_list: list

class RouteRequest(BaseModel):
    route: str

class FileReadRequest(BaseModel):
    file_name: str

class FileWriteRequest(BaseModel):
    fileName: str
    block_size: int
    last_block_size: int
    block_num: int
    replication_rate: int

@app.post("/namenode/api/v1/handshake/")
async def dataNodeHandshake(request: HandShakeRequest):
    success = nameNode.createDataNode(request.ip_address, request.port, "active")
    if success: 
        return { "message": "HandShake datanode succesfully!", "success": success }
    else: 
        return { "message": "HandShake datanode failed!", "success": success }


@app.post("/namenode/api/v1/heartbeat")
async def dataNodeHeartbeat(request: HeartbeatRequest):
    pass

# File ops
@app.post("/namenode/api/v1/datanode_read_list")
async def getReadFileDataNodes(request: FileReadRequest):
    NameNode.getReadDataNodes("", 3, 3, "")
    return { }

@app.post("/namenode/api/v1/datanode_write_list")
async def selectWriteFileDataNodes(request: FileWriteRequest):
    dataNodeWriteList = nameNode.getWriteDataNodes("", 3, 3, "")
    return { "dataNodesAvailable": dataNodeWriteList }

# File System ops
@app.get("/namenode/api/v1/ls")
async def listDirectory(route: str):
    directory_content = nameNode.directoryTree.ls(route)
    return { "directory_content": directory_content }

@app.post("/namenode/api/v1/mkdir")
async def makeDirectory(route: RouteRequest):
    success = nameNode.directoryTree.add_directory(route.route)
    if success: 
        return { "message": "Directory successfully created!", "success": success }
    else: 
        return { "message": "Directory failed created!", "success": success }

@app.post("/namenode/api/v1/cd")
async def changeDirectory(request: RouteRequest):
    targetRequest = nameNode.directoryTree.get_directory(request.route)
    if targetRequest: 
        return { "message": "Change Directory!", "route": request.route }
    else: 
        return HTTPException(status_code=404, detail="No such file or directory")

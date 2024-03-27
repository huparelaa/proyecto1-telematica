import grpc 
import time
import os
import filetransfer_pb2_grpc 
import filetransfer_pb2 
from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

class FileName(BaseModel):
    file_name: str

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

app.mount("/files", StaticFiles(directory="files"), name="files")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    fileList = os.listdir("./files")
    print(fileList)
    return templates.TemplateResponse("index.html", { "request": request, "file_list": fileList })

def upload_file_with_grpc(file_name, file_content):
    with grpc.insecure_channel("localhost:50051") as channel:  # Connect to the gRPC server
        stub = filetransfer_pb2_grpc.FileTransferStub(channel)
        response = stub.UploadFile(filetransfer_pb2.FileChunk(name=file_name, content=file_content))
        return response.success

def download_file_with_grpc(file_name): 
    with grpc.insecure_channel("localhost:50051") as channel: 
        stub = filetransfer_pb2_grpc.FileTransferStub(channel)
        response = stub.DownloadFile(filetransfer_pb2.Request(name=file_name))
        return response     

@app.post("/upload_grpc/")
async def upload_file_grpc(file: UploadFile = File(...)):
    fileName = file.filename
    print("-----------------------------")
    print(fileName) 
    print("-----------------------------")
    file
    content = await file.read()
    start_time = time.time()
    success = upload_file_with_grpc(fileName, content)
    if success:
        print(f"Sending file using gRPC speed: {time.time() - start_time}")
        return {"message": f"File {file.filename} has been uploaded."}
    else:
        return {"message": "Failed to upload the file."}

"""
Escribir archivos

1. Subir el archivo.
2. Hacer un split del archivo como tal.
3. Mandar una petición al NameNode para pedir a que DataNodes enviar los archivos.
4. 

"""


"""
Leer archivos

"""

@app.post("/download_grpc/")
async def download_file_grpc(file_name: str = Form(...)): 
    print(file_name)
    fileContent = download_file_with_grpc(file_name)
    if fileContent: 
        with open(f"./files/{file_name}", "wb") as f: 
            f.write(fileContent.content)
        return {"message": f"File {file_name} has been download."}
    else: 
        return {"message": "Failed to download the file."}
    

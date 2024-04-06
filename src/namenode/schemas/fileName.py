from pydantic import BaseModel

class FileReadRequest(BaseModel):
    file_name: str
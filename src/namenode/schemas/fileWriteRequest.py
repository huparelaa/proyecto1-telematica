from pydantic import BaseModel

class FileWriteRequest(BaseModel):
    file_name: str
    file_path: str
    block_num: int
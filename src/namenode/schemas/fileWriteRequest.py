from pydantic import BaseModel

class FileWriteRequest(BaseModel):
    file_name: str
    block_size: int
    block_num: int
    num_replicas: int
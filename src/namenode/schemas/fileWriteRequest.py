from pydantic import BaseModel

class FileWriteRequest(BaseModel):
    fileName: str
    block_size: int
    last_block_size: int
    block_num: int
    replication_rate: int
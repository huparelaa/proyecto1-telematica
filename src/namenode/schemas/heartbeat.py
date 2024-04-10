from pydantic import BaseModel

class HeartbeatRequest(BaseModel):
    ip_address: str
    port: str
    block_list: list
    status: str
from pydantic import BaseModel  

class HandShakeRequest(BaseModel):
    ip_address: str
    port: str
    process: str
    space: str
    block_list: list
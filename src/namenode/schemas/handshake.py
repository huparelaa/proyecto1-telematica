from pydantic import BaseModel  

class HandShakeRequest(BaseModel):
    ip_address: str
    port: str
    available_space: int
    block_list: list
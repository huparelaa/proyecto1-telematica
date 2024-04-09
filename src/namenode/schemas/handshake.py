from pydantic import BaseModel  

class HandShakeRequest(BaseModel):
    ip_address: str
    port: str
    block_list: list
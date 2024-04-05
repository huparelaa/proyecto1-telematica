from pydantic import BaseModel

class RouteRequest(BaseModel):
    route: str
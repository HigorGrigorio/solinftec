from pydantic import BaseModel


class TileMessage(BaseModel):
    id: str
    path: str
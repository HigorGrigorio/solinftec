from pydantic import BaseModel

class TalhaoMessage(BaseModel):
    id: str
    shapeFilePath:str
    layerName:str
    outputFilePath:str
    coordnatesOutputPath:str
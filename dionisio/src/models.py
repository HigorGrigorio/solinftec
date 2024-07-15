from pydantic import BaseModel

class TalhaoMessage(BaseModel):
    shapeFilePath:str
    layerName:str
    outputFilePath:str
    coordnatesOutputPath:str
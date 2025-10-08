from pydantic import BaseModel

class RegisterCategory (BaseModel):
    name: str

class ModifyCategory (BaseModel): 
    name: str  
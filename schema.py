from pydantic import BaseModel, ConfigDict

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    year: int
    available: bool = True
    
    model_config = ConfigDict(from_attributes=True)
    
class BookCreate(BaseModel):
    title: str
    author: str
    year: int
    available: bool
    
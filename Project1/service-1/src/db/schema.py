from pydantic import BaseModel

class Upload(BaseModel):
    email: str
    inputs: str
    language: str
    enable: int

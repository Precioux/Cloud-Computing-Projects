from pydantic import BaseModel

class Job(BaseModel):
    id: int
    upload: int
    job: str
    enable: int

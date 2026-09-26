from pydantic import BaseModel
class Workflow(BaseModel):
    id:str
    name:str
    description: str | None = None
    status: str

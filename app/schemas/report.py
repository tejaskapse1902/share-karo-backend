from pydantic import BaseModel

class ReportCreateSchema(BaseModel):
    title: str
    content: str
    
# api/models.py
from pydantic import BaseModel

class QueryRequest(BaseModel):  
    question: str
    scenario: str
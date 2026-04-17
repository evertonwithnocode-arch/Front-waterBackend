from pydantic import BaseModel
from typing import List, Optional

class DocumentInput(BaseModel):
    user_id: str
    content: str
    metadata: dict

class QueryInput(BaseModel):
    user_id: str
    query: str
    entity: str
    workflow: str
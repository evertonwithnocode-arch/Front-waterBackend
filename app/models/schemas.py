from pydantic import BaseModel
from typing import List, Dict, Any

class UploadRequest(BaseModel):
    user_id: str
    content: str
    metadata: Dict[str, Any]

class QueryRequest(BaseModel):
    question: str
    user_id: str
    role: str
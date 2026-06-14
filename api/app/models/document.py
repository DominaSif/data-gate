from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DocumentCreate(BaseModel):
    title: str
    content: Optional[str] = None

class DocumentResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: Optional[str]
    is_public: bool
    created_at: datetime
    updated_at: datetime

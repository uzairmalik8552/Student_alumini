from datetime import datetime, timezone
from pydantic import BaseModel
from typing import Optional


class Post(BaseModel):
    user_id: str
    content: str
    created_at: Optional[datetime] = datetime.now(timezone.utc)
    updated_at: Optional[datetime] = datetime.now(timezone.utc)

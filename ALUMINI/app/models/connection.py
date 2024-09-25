from datetime import datetime, timezone
from pydantic import BaseModel
from typing import List
from typing import Optional


class Connection(BaseModel):
    user_id: str
    connections: List[str]
    created_at: Optional[datetime] = datetime.now(timezone.utc)
    updated_at: Optional[datetime] = datetime.now(timezone.utc)

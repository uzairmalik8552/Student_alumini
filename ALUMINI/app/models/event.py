from datetime import datetime, timezone
from pydantic import BaseModel
from typing import Optional
from bson import ObjectId


class Event(BaseModel):
    title: str
    description: Optional[str] = None
    date: datetime
    location: Optional[str] = None
    event_type: Optional[str] = None  # Event type (e.g., networking, seminar)
    event_link: Optional[str] = None  # URL for the event
    user_id: str  # User who created the event
    likes: int = 0  # To track the number of likes, default is 0
    created_at: Optional[datetime] = datetime.now(timezone.utc)
    updated_at: Optional[datetime] = datetime.now(timezone.utc)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

from fastapi import APIRouter, HTTPException
from app.models.event import Event
# Import the update service
from app.services.event_service import create_event, update_event_likes, get_all_events
from pydantic import BaseModel

router = APIRouter()

# POST: Create a new event


@router.post("/events_creation")
def add_event(event: Event):
    try:
        event_id = create_event(event)
        return {"message": "Event created successfully", "event_id": event_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Pydantic model for the request body to update likes


class LikeUpdateRequest(BaseModel):
    event_id: str
    likes: int

# PUT: Update the number of likes for an event


@router.put("/events_likes")
def update_likes(data: LikeUpdateRequest):
    try:
        # Call the service to update likes
        update_event_likes(data.event_id, data.likes)
        return {"message": "Event likes updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/events/")
def fetch_all_events():
    try:
        events = get_all_events()

        return {"events": events}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

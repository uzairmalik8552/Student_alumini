from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timezone
from app.models.event import Event

# MongoDB connection setup
client = MongoClient("mongodb://localhost:27017/")
db = client.studentalumini  # Your database name

# Function to create a new event


def create_event(event_data: Event):
    # Convert the Pydantic model to a dictionary
    event_dict = event_data.dict()
    event_dict['created_at'] = datetime.now(timezone.utc)
    event_dict['updated_at'] = datetime.now(timezone.utc)

    # Insert the event into MongoDB
    result = db.event.insert_one(event_dict)

    return str(result.inserted_id)  # Return the ID of the newly created event


# Function to update the number of likes for an event
def update_event_likes(event_id: str, likes: int):
    result = db.events.update_one(
        {"_id": ObjectId(event_id)},
        {"$set": {"likes": likes}}
    )

    if result.matched_count == 0:
        raise Exception("Event not found")

    return True


def get_all_events():
    events = list(db.event.find())  # Fetch all events
    for event in events:
        event["_id"] = str(event["_id"])  # Convert ObjectId to string
    return events

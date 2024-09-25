from datetime import datetime, timezone
from bson import ObjectId
# Ensure this import matches your actual setup
from config import profiles_collection


def get_profile_by_user_id(user_id: str):
    # Retrieve the profile by user_id
    profile = profiles_collection.find_one({"user_id": user_id})
    if profile:
        # Convert ObjectId to string
        profile["_id"] = str(profile["_id"])
    return profile


def update_profile_by_user_id(user_id: str, profile_data: dict):
    # Add the current time to the update
    profile_data['updated_at'] = datetime.now(timezone.utc)

    # Update the profile in the database
    result = profiles_collection.update_one(
        {"user_id": user_id},
        {"$set": profile_data}
    )

    # Check if a profile was updated
    if result.matched_count == 0:
        return None

    # Return the updated profile
    updated_profile = profiles_collection.find_one({"user_id": user_id})
    if updated_profile:
        # Convert ObjectId to string
        updated_profile["_id"] = str(updated_profile["_id"])
    return updated_profile


def update_profile_picture_by_user_id(user_id: str, picture_data: bytes):
    # Update the profile picture in the database
    result = profiles_collection.update_one(
        {"user_id": user_id},
        {"$set": {"profile_pic": picture_data,
                  "updated_at": datetime.now(timezone.utc)}}
    )

    return result.matched_count > 0


def fetch_profile_picture_by_user_id(user_id: str):
    profile = profiles_collection.find_one(
        {"user_id": user_id}, {"profile_pic": 1})
    if profile and "profile_pic" in profile:
        return profile["profile_pic"]
    return None

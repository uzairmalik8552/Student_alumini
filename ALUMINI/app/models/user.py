from datetime import datetime, timezone
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from bson import ObjectId


# Custom ObjectId type for MongoDB
class PyObjectId(ObjectId):
    @classmethod
    def _get_pydantic_json_schema_(cls, schema: dict) -> dict:
        schema.update({
            "type": "string",
            "format": "objectid"
        })
        return schema

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)


# User model
class User(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    name: str  # Full name of the user
    email: EmailStr
    password: str
    role: str  # For example: 'alumni' or 'student'
    contact: Optional[str] = None
    last_login: Optional[datetime] = None  # Last login date
    created_at: Optional[datetime] = datetime.now(timezone.utc)
    updated_at: Optional[datetime] = datetime.now(timezone.utc)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "password": "hashedpassword",
                "role": "alumni",
                "contact": "1234567890",
                "last_login": "2024-09-10T10:00:00Z",
                "created_at": "2023-09-10T12:00:00Z",
                "updated_at": "2024-09-10T12:00:00Z"
            }
        }

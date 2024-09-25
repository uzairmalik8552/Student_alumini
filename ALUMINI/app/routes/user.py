from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from app.services.user_service import create_user_service


router = APIRouter()

# Pydantic model for request body


class UserCreateRequest(BaseModel):
    name: str
    email: str
    role: str
    password: str
    contact: Optional[str] = None
    location: Optional[str] = None


@router.post("/create-user")
async def create_user(user: UserCreateRequest):
    try:
        created_user = await create_user_service(user)
        return {"message": "User created successfully", "user": created_user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

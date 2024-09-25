from fastapi import APIRouter, HTTPException, status, File, UploadFile
from pydantic import BaseModel
from app.services.profile_service import get_profile_by_user_id, update_profile_by_user_id, update_profile_picture_by_user_id, fetch_profile_picture_by_user_id
from app.models.profile import Profile

router = APIRouter()


class UserIDRequest(BaseModel):
    user_id: str


@router.post("/profile")
async def get_profile(request: UserIDRequest):
    user_id = request.user_id
    profile = get_profile_by_user_id(user_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    return profile


@router.put("/profile")
async def update_profile(request: Profile):
    user_id = request.user_id
    existing_profile = get_profile_by_user_id(user_id)
    if not existing_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )

    updated_profile = update_profile_by_user_id(user_id, request.dict())

    if not updated_profile:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating profile"
        )

    return updated_profile


@router.post("/profile/picture")
async def update_profile_picture(request: UserIDRequest, file: UploadFile = File(...)):
    user_id = request.user_id
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID is required"
        )

    file_content = await file.read()
    result = update_profile_picture_by_user_id(user_id, file_content)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found or update failed"
        )

    return {"detail": "Profile picture updated successfully"}


@router.get("/profile/picture")
async def fetch_profile_picture(request: UserIDRequest):
    user_id = request.user_id
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID is required"
        )

    picture = fetch_profile_picture_by_user_id(user_id)
    if picture is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile picture not found"
        )

    return {"profile_picture": picture}

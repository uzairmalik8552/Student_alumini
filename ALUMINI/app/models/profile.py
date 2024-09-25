from datetime import datetime, timezone
from pydantic import BaseModel
from typing import Optional, List


# Nested model for School/College
class SchoolCollege(BaseModel):
    school_name: str
    degree: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    description: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "school_name": "Harvard University",
                "degree": "Bachelor of Science",
                "start_date": "2016-09-01T00:00:00Z",
                "end_date": "2020-06-15T00:00:00Z",
                "description": "Graduated with honors."
            }
        }


# User profile model
class Profile(BaseModel):
    user_id: str
    name: str  # Full name of the user
    role: str  # Role like 'alumni', 'student', etc.
    bio: Optional[str] = None
    career_path: Optional[str] = None  # Career path of the user
    schools_colleges: List[SchoolCollege] = []  # List of schools/colleges
    specialization: Optional[List[str]] = None  # List of specializations
    achievements: Optional[List[str]] = []
    skills: Optional[List[str]] = []
    location: Optional[str] = None  # Location of the user (new field)
    profile_pic: Optional[bytes] = None  # Binary data for profile picture
    updated_at: Optional[datetime] = datetime.now(timezone.utc)

    class Config:
        schema_extra = {
            "example": {
                "user_id": "607f1f77bcf86cd799439011",
                "name": "John Doe",
                "role": "alumni",
                "bio": "Software engineer with a passion for AI.",
                "career_path": "Software Engineer",
                "schools_colleges": [
                    {
                        "school_name": "svce",
                        "degree": "Bachelor of Science",
                        "start_date": "2016-09-01T00:00:00Z",
                        "end_date": "2020-06-15T00:00:00Z",
                        "description": "Graduated with honors."
                    }
                ],
                "specialization": ["AI", "Machine Learning"],
                "achievements": ["Dean's List 2019", "AI Conference Speaker"],
                "skills": ["Python", "Data Analysis"],
                "location": "New York, USA",  # Example for the new location field
                "updated_at": "2024-09-10T12:00:00Z"
            }
        }

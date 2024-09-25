from app.models.user import User
from app.models.profile import Profile
from pymongo import MongoClient
from passlib.context import CryptContext

# Initialize the password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash a password


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


client = MongoClient('mongodb://localhost:27017/')
db = client.studentalumini

# Service function to create user


async def create_user_service(user_data):
    user_collection = db.users
    profile_collection = db.profiles

    # Hash the password before saving
    hashed_password = hash_password(user_data.password)

    # Insert data into user model
    user = User(
        name=user_data.name,
        email=user_data.email,
        role=user_data.role,
        password=hashed_password,  # Store hashed password
        contact=user_data.contact
    )

    # Save user to MongoDB using `model_dump`
    user_id = user_collection.insert_one(
        user.model_dump(by_alias=True)).inserted_id
    print(user_id)

    # Insert data into profile model
    profile = Profile(
        user_id=str(user_id),
        name=user_data.name,
        role=user_data.role,
        bio="null",
        career_path="null",
        schools_colleges=[],  # Empty list for schools_colleges
        specialization=[],    # Empty list for specialization
        achievements=[],      # Empty list for achievements
        skills=[],            # Empty list for skills
        location=user_data.location,  # Save location to profile
        profile_pic="null"
    )

    # Save profile to MongoDB using `model_dump`
    profile_collection.insert_one(profile.model_dump())

    return user.model_dump()

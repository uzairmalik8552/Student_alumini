from pymongo import MongoClient
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        # Load environment variables from a .env file (if used)
        env_file = ".env"


# Initialize settings
settings = Settings()

# MongoDB configuration
client = MongoClient('mongodb://localhost:27017/')  # Adjust the URI as needed
db = client['studentalumini']  # Database name

# Define collections
users_collection = db['users']  # Collection for users
profiles_collection = db['profiles']  # Collection for profiles

# Access the settings as:
# settings.SECRET_KEY
# settings.ALGORITHM
# settings.ACCESS_TOKEN_EXPIRE_MINUTES

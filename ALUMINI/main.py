from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, user, profile  # Import the profile route
from app.routes.event_routes import router as event_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes from different modules
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(profile.router)  # Include the profile router
app.include_router(event_router)

import os
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import HTTPException
from pydantic import BaseModel
from config import users_collection, settings

# For password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to verify password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Function to create access token


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt

# Function to get user by email


def get_user_by_email(email: str):
    # Assuming users_collection contains documents with "email" field
    user = users_collection.find_one({"email": email})
    return user

# Pydantic model to parse incoming data


class UserLogin(BaseModel):
    email: str
    password: str

# Function to send an email to the user


async def send_login_alert(user_email: str):
    sender_email = os.getenv("2021ad0731@svce.ac.in")
    sender_password = os.getenv("TamizhagaVetriKazhagam@2026")

    subject = "Login Notification"
    body = f"Dear", {
        user_email}, "\n", "You have successfully logged in to the system.\n\nBest regards,\nYour Website Team"

    # Create a MIME object
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = user_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to Gmail's SMTP server asynchronously
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, user_email, text)
            print(f"Login alert sent to {user_email}")
    except Exception as e:
        print(f"Error sending email: {e}")

# Basic login function


async def login(user: UserLogin):
    email = user.email
    password = user.password

    # Get user from database
    db_user = get_user_by_email(email)
    if db_user and verify_password(password, db_user["password"]):
        # Successful login
        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": email}, expires_delta=access_token_expires)

        # Send login alert email
        # Send login alert email to the user asynchronously
        await send_login_alert(email)

        return {"access_token": access_token, "token_type": "bearer"}
    else:
        # Invalid login
        raise HTTPException(
            status_code=401, detail="Invalid email or password")

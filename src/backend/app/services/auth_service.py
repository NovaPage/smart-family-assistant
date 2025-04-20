# File: src/backend/app/services/auth_service.py

from app.models.user import UserCreate, UserInDB
from app.models.auth import Token
from app.repositories import user_repository
from app.core.config import settings

from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from uuid import UUID

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Returns a hashed version of the password.
    """
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    """
    Verifies that a plain password matches a hashed password.
    """
    return pwd_context.verify(password, hashed)


def create_jwt_token(user_id: UUID) -> Token:
    """
    Generates a JWT token with user_id as subject.
    """
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expiration_minutes)
    payload = {
        "sub": str(user_id),
        "exp": expire
    }
    encoded = jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return Token(access_token=encoded)


def register(user_data: UserCreate) -> Token:
    """
    Registers a new user and returns a JWT.
    """
    existing = user_repository.get_user_by_email(user_data.email)
    if existing:
        raise Exception("Email already registered")

    hashed_pw = hash_password(user_data.password)
    user = user_repository.create_user(user_data, hashed_pw)
    return create_jwt_token(user.id)


def login(email: str, password: str) -> Token:
    """
    Validates credentials and returns JWT.
    """
    user = user_repository.get_user_by_email(email)
    if not user or not verify_password(password, user.hashed_password):
        raise Exception("Invalid credentials")

    return create_jwt_token(user.id)

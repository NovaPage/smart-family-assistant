# File: src/backend/app/services/user_service.py

from uuid import UUID
from app.models.user import UserInDB, UserProfile, UserUpdate
from app.repositories import user_repository


def get_profile(user: UserInDB) -> UserProfile:
    """
    Returns the profile of the authenticated user.
    """
    return UserProfile(id=user.id, name=user.name, email=user.email)


def update_profile(user: UserInDB, data: UserUpdate) -> UserProfile:
    """
    Updates user profile data.
    """
    updated_user = user_repository.update_profile(user.id, data)
    return UserProfile(id=updated_user.id, name=updated_user.name, email=updated_user.email)

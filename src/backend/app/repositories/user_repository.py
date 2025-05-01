# File: src/backend/app/repositories/user_repository.py

from uuid import UUID, uuid4
from typing import Optional

from app.models.user import UserCreate, UserUpdate, UserInDB
from app.core.config import settings
from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.exceptions import CosmosResourceNotFoundError

# Initialize Cosmos DB client
cosmos_client = CosmosClient(settings.cosmos_db_uri, credential=settings.cosmos_db_key)
database = cosmos_client.get_database_client(settings.cosmos_db_database)
users_container = database.get_container_client("users")

def get_user_by_telegram_token(token: str) -> Optional[UserInDB]:
    """
    Finds a user by their unique Telegram token (used for linking).
    """
    query = "SELECT * FROM users u WHERE u.telegram_token = @token"
    params = [{"name": "@token", "value": token}]
    result = list(users_container.query_items(query, parameters=params, enable_cross_partition_query=True))

    if not result:
        return None

    user = result[0]
    return UserInDB(
        id=UUID(user["id"]),
        name=user["name"],
        email=user["email"],
        hashed_password=user["hashed_password"],
        telegram_token=user.get("telegram_token"),
        telegram_chat_id=user.get("telegram_chat_id")
    )


def update_user_telegram_chat_id(user_id: UUID, chat_id: int) -> None:
    """
    Updates the user's record to include their Telegram chat ID.
    """
    user = users_container.read_item(item=str(user_id), partition_key=str(user_id))
    user["telegram_chat_id"] = chat_id
    users_container.replace_item(item=str(user_id), body=user)


def get_user_by_chat_id(chat_id: int) -> Optional[UserInDB]:
    """
    Finds a user based on their Telegram chat ID.
    """
    query = "SELECT * FROM users u WHERE u.telegram_chat_id = @chat_id"
    params = [{"name": "@chat_id", "value": chat_id}]
    result = list(users_container.query_items(query, parameters=params, enable_cross_partition_query=True))

    if not result:
        return None

    user = result[0]
    return UserInDB(
        id=UUID(user["id"]),
        name=user["name"],
        email=user["email"],
        hashed_password=user["hashed_password"],
        telegram_token=user.get("telegram_token"),
        telegram_chat_id=user.get("telegram_chat_id")
    )


def create_user(user_data: dict, hashed_password: str) -> UserInDB:
    """
    Creates a new user in the database with hashed password and optional telegram_token.
    """
    user_id = str(uuid4())
    user_record = {
        "id": user_id,
        "name": user_data["name"],
        "email": user_data["email"],
        "hashed_password": hashed_password,
    }

    if "telegram_token" in user_data:
        user_record["telegram_token"] = user_data["telegram_token"]

    users_container.create_item(user_record)

    return UserInDB(
        id=UUID(user_id),
        name=user_data["name"],
        email=user_data["email"],
        hashed_password=hashed_password,
        telegram_token=user_data.get("telegram_token")
    )


def get_user_by_email(email: str) -> Optional[UserInDB]:
    """
    Retrieves a user from the database using their email.
    """
    query = "SELECT * FROM users u WHERE u.email = @email"
    params = [{"name": "@email", "value": email}]
    result = list(users_container.query_items(query, parameters=params, enable_cross_partition_query=True))

    if not result:
        return None

    user = result[0]
    return UserInDB(
        id=UUID(user["id"]),
        name=user["name"],
        email=user["email"],
        hashed_password=user["hashed_password"],
        telegram_token=user.get("telegram_token")
    )


def get_user_by_id(user_id: UUID) -> Optional[UserInDB]:
    """
    Retrieves a user from the database using their ID.
    """
    try:
        user = users_container.read_item(item=str(user_id), partition_key=str(user_id))
        return UserInDB(
            id=UUID(user["id"]),
            name=user["name"],
            email=user["email"],
            hashed_password=user["hashed_password"],
            telegram_token=user.get("telegram_token"),
            telegram_chat_id=user.get("telegram_chat_id")
        )
    except CosmosResourceNotFoundError:
        return None


def update_profile(user_id: UUID, data: UserUpdate) -> Optional[UserInDB]:
    """
    Updates the profile of a user in the database.
    """
    user = get_user_by_id(user_id)
    if user is None:
        return None

    updated_user = {
        "id": str(user.id),
        "email": user.email,
        "name": data.name or user.name,
        "hashed_password": user.hashed_password
    }

    users_container.replace_item(item=str(user.id), body=updated_user)

    return UserInDB(
        id=user.id,
        email=user.email,
        name=updated_user["name"],
        hashed_password=user.hashed_password
    )

# File: src/backend/app/repositories/interaction_repository.py

from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import List

from app.models.interaction import Interaction
from app.repositories.cosmos_client import database

interactions_container = database.get_container_client("interactions")


def save_interaction(interaction: Interaction) -> None:
    """
    Saves a user-assistant interaction to the database with thread_id.
    """
    item = {
        "id": str(interaction.id),
        "user_id": str(interaction.user_id),
        "thread_id": str(interaction.thread_id),
        "message": interaction.message,
        "response": interaction.response,
        "timestamp": interaction.timestamp.isoformat()
    }
    interactions_container.create_item(item)


def get_interactions_by_user(user_id: UUID) -> List[Interaction]:
    """
    Retrieves all interactions for a given user.
    """
    query = "SELECT * FROM interactions i WHERE i.user_id = @user_id"
    params = [{"name": "@user_id", "value": str(user_id)}]
    items = interactions_container.query_items(query, parameters=params, enable_cross_partition_query=True)

    return [
        Interaction(
            id=item["id"],
            user_id=UUID(item["user_id"]),
            thread_id=item.get("thread_id"),
            message=item["message"],
            response=item["response"],
            timestamp=datetime.fromisoformat(item["timestamp"])
        )
        for item in items
    ]


def get_last_messages_by_thread(thread_id: str, limit: int = 5) -> List[Interaction]:
    """
    Retrieves the last interactions in a specific thread, ordered by timestamp descending.
    """
    query = (
        "SELECT * FROM interactions i "
        "WHERE i.thread_id = @thread_id "
        "ORDER BY i.timestamp DESC"
    )
    params = [{"name": "@thread_id", "value": thread_id}]
    items = interactions_container.query_items(query, parameters=params, enable_cross_partition_query=True)

    interactions = [
        Interaction(
            id=item["id"],
            user_id=item["user_id"],
            thread_id=item["thread_id"],
            message=item["message"],
            response=item["response"],
            timestamp=datetime.fromisoformat(item["timestamp"])
        )
        for item in items
    ]

    return interactions[:limit]

# File: src/backend/app/repositories/interaction_repository.py

# Add this at the top of src/backend/app/services/assistant_service.py

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[4]))  # Esto apunta al root del proyecto


from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import List

from src.backend.app.models.interaction import Interaction
from src.backend.app.repositories.cosmos_client import database
from family_agent.agents.maestro import MasterAssistant

from src.backend.app.models.assistant import AssistantRequest, AssistantResponse
from src.backend.app.models.user import UserInDB
from src.backend.app.repositories import interaction_repository
from app.models.interaction import Interaction



interactions_container = database.get_container_client("interactions")


def save_interaction(interaction: Interaction) -> None:
    """
    Saves a user-assistant interaction to the database.
    """
    item = {
        "id": str(uuid4()),
        "user_id": str(interaction.user_id),
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
            user_id=UUID(item["user_id"]),
            message=item["message"],
            response=item["response"],
            timestamp=datetime.fromisoformat(item["timestamp"])
        )
        for item in items
    ]

def process_message(current_user: UserInDB, request: AssistantRequest) -> AssistantResponse:
    # Create the assistant
    agent = MasterAssistant()

    # Get the response from the agent
    response = agent.process_message(request.message)

    # Save the interaction
    interaction = Interaction(
        id=str(uuid4()),
        user_id=str(current_user.id),
        message=request.message,
        response=response,
        timestamp=datetime.now(timezone.utc)
    )
    interaction_repository.save_interaction(interaction)


    # Return structured response
    return AssistantResponse(response=response)
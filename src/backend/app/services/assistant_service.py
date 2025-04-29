# File: src/backend/app/services/assistant_service.py

import sys
from pathlib import Path
from uuid import uuid4
from datetime import datetime, timezone

sys.path.append(str(Path(__file__).resolve().parents[4]))

from app.models.assistant import AssistantRequest, AssistantResponse
from app.models.interaction import Interaction
from app.models.user import UserInDB
from app.models.thread import ThreadCreate, ThreadInDB
from app.repositories import interaction_repository, thread_repository
from app.core.config import settings
from family_agent.assistants.maestro import MasterAssistant


class AssistantService:
    """
    Service responsible for handling interactions between users and the Master Assistant.
    """

    def __init__(self) -> None:
        self.master_assistant: MasterAssistant = MasterAssistant()

    def send_message(self, user: UserInDB, message: str, source: str) -> str:
        """
        Processes a user's message by either creating a new thread or continuing an existing one.
        Saves the interaction and updates thread timestamps.
        """
        context: str | None = None
        thread: ThreadInDB | None = thread_repository.get_active_thread(user.id, source)

        if thread:
            if thread_repository.is_thread_inactive(thread):
                thread_repository.close_thread(thread.id)
                context = self._summarize_recent_conversation(thread.id)
                thread = None  # Force creation of a new thread

        if not thread:
            reply, openai_thread_id = self.master_assistant.process_message(
                message=message,
                context=context,
                thread_id=None
            )
            thread = thread_repository.create_thread(
                ThreadCreate(
                    user_id=str(user.id),
                    source=source,
                    summary=context,
                    openai_thread_id=openai_thread_id
                )
            )
        else:
            reply, _ = self.master_assistant.process_message(
                message=message,
                context=context,
                thread_id=thread.openai_thread_id
            )

        interaction: Interaction = self._build_interaction(user, thread.id, message, reply)
        interaction_repository.save_interaction(interaction)
        thread_repository.update_timestamp(thread.id)

        return reply

    def _summarize_recent_conversation(self, thread_id: str) -> str:
        """
        Summarizes the last messages of a closed thread to preserve conversation context.
        """
        recent_messages: list[Interaction] = interaction_repository.get_last_messages_by_thread(thread_id, limit=5)
        conversation_log: str = "\n".join([
            f"User: {message.message}\nAssistant: {message.response}"
            for message in recent_messages
        ])

        summary_prompt: str = (
            "Summarize this past conversation to help resume it later:\n\n"
            f"{conversation_log}"
        )
        summary, _ = self.master_assistant.process_message(message=summary_prompt, context=None)
        thread_repository.update_summary(thread_id, summary)

        return summary

    def _build_interaction(self, user: UserInDB, thread_id: str, message: str, reply: str) -> Interaction:
        """
        Constructs an Interaction object from the provided information.
        """
        return Interaction(
            id=str(uuid4()),
            user_id=user.id,
            thread_id=thread_id,
            message=message,
            response=reply,
            timestamp=datetime.now(timezone.utc)
        )

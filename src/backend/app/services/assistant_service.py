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
from family_agent.agents.maestro import MasterAssistant


class AssistantService:
    def __init__(self):
        self.agent = MasterAssistant()

    def send_message(self, user: UserInDB, message: str, source: str) -> str:
        context = None
        thread = thread_repository.get_active_thread(user.id, source)

        if thread:
            if thread_repository.is_thread_inactive(thread):
                thread_repository.close_thread(thread.id)

                recent_messages = interaction_repository.get_last_messages_by_thread(thread.id, limit=5)
                conversation_log = "\n".join([
                    f"User: {msg.message}\nAssistant: {msg.response}" for msg in recent_messages
                ])

                summary_prompt = (
                    "Summarize this past conversation to help resume it later:\n\n"
                    f"{conversation_log}"
                )
                summary, _ = self.agent.process_message(message=summary_prompt, context=None)
                thread_repository.update_summary(thread.id, summary)
                context = summary
                thread = None  # Se fuerza creación de nuevo hilo

        # Crear nuevo hilo si no existe (o si se cerró el anterior por inactividad)
        if not thread:
            reply, openai_thread_id = self.agent.process_message(
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
            # Reutilizar hilo existente
            reply, _ = self.agent.process_message(
                message=message,
                context=context,
                thread_id=thread.openai_thread_id
            )

        # Guardar la interacción
        interaction = Interaction(
            id=str(uuid4()),
            user_id=user.id,
            thread_id=thread.id,
            message=message,
            response=reply,
            timestamp=datetime.now(timezone.utc)
        )
        interaction_repository.save_interaction(interaction)
        thread_repository.update_timestamp(thread.id)

        return reply

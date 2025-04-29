# File: family_agent/flows/test_conversacion_maestro.py

import sys
from pathlib import Path

# Add the project root to sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from family_agent.assistants.maestro import MasterAssistant

def test_master_assistant() -> None:
    """
    Test to validate that the MasterAssistant responds correctly using OpenAI Assistants API.
    """
    assistant: MasterAssistant = MasterAssistant()

    user_message: str = "What can I do to sleep better at night?"
    assistant_response: tuple[str, str] = assistant.process_message(
        message=user_message,
        context=None,
        thread_id=None
    )

    reply: str = assistant_response[0]

    print("🗨️ User:", user_message)
    print("🤖 Assistant:", reply)

if __name__ == "__main__":
    test_master_assistant()

# File: family_agent/assistants/maestro.py

import os
import json
import time
from pathlib import Path
from typing import Optional, Tuple
from dotenv import load_dotenv
from openai import OpenAI


class MasterAssistant:
    """
    MasterAssistant encapsulates interaction with OpenAI Assistants API (v2),
    handling message sending, thread creation, and run management.
    """

    def __init__(self, config_dir: Optional[Path] = None) -> None:
        self.base_path: Path = config_dir or Path(__file__).resolve().parent.parent
        self._load_environment()
        self.prompt: str = self._load_prompt()
        self.assistant_id: str = self._load_assistant_id()
        self.client: OpenAI = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            default_headers={"OpenAI-Beta": "assistants=v2"}
        )

    def _load_environment(self) -> None:
        """
        Loads environment variables from the .env file in the root directory.
        """
        dotenv_path = self.base_path / ".env"
        load_dotenv(dotenv_path=dotenv_path)

    def _load_prompt(self) -> str:
        """
        Loads the system prompt from prompt_maestro.txt.
        """
        prompt_path = self.base_path / "configs" / "prompt_maestro.txt"
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()

    def _load_assistant_id(self) -> str:
        """
        Loads the assistant_id from tools_config.json.
        """
        tools_path = self.base_path / "configs" / "tools_config.json"
        with open(tools_path, "r", encoding="utf-8") as f:
            tools = json.load(f)

        assistant_id: Optional[str] = tools.get("maestro")
        if not assistant_id:
            raise ValueError("🛑 Assistant ID for 'maestro' not found in tools_config.json")

        return assistant_id

    def process_message(
        self,
        message: str,
        context: Optional[str] = None,
        thread_id: Optional[str] = None
    ) -> Tuple[str, str]:
        """
        Sends a message to the Assistant and retrieves the response.
        Creates a thread if none is provided. Returns the assistant's reply and thread_id.
        """
        if not thread_id:
            thread = self.client.beta.threads.create()
            thread_id = thread.id

        self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message
        )

        system_instructions: str = self._build_system_prompt(context)

        run = self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=self.assistant_id,
            instructions=system_instructions
        )

        # Poll until run is completed
        while True:
            run_status = self.client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )
            if run_status.status == "completed":
                break
            elif run_status.status == "failed":
                return "❌ Assistant run failed.", thread_id

            time.sleep(1)  # Prevents high CPU usage

        messages = self.client.beta.threads.messages.list(thread_id=thread_id)
        assistant_reply = next(
            (msg for msg in messages.data if msg.role == "assistant"),
            None
        )

        reply = assistant_reply.content[0].text.value if assistant_reply else "❌ No response."
        return reply, thread_id

    def _build_system_prompt(self, context: Optional[str]) -> str:
        """
        Builds the system instructions prompt, using the default or adding context.
        """
        if not context:
            return self.prompt
        return f"Previously you were helping with this:\n{context}\n\nContinue helping in a natural way."

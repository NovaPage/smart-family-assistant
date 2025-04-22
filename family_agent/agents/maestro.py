# File: autogen/agents/maestro.py

import os
import json
from pathlib import Path
from typing import Optional, Tuple

from dotenv import load_dotenv
from openai import OpenAI
from autogen import AssistantAgent


class MasterAssistant:
    """
    MasterAssistant encapsulates the behavior and configuration of the main assistant agent.
    """

    def __init__(self, config_dir: Optional[Path] = None):
        self.base_path = config_dir or Path(__file__).resolve().parent.parent
        self._load_environment()
        self.prompt = self._load_prompt()
        self.llm_config = self._load_llm_config()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.assistant_id = self._get_assistant_id()

    def _load_environment(self) -> None:
        dotenv_path = self.base_path / ".env"
        load_dotenv(dotenv_path=dotenv_path)

    def _load_prompt(self) -> str:
        prompt_path = self.base_path / "configs" / "prompt_maestro.txt"
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()

    def _load_llm_config(self) -> dict:
        config_path = self.base_path / "configs" / "llm_config.json"
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        for entry in config.get("config_list", []):
            if "${OPENAI_API_KEY}" in entry.get("api_key", ""):
                entry["api_key"] = os.getenv("OPENAI_API_KEY")
        return config

    def _get_assistant_id(self) -> str:
        assistant = AssistantAgent(
            name="Maestro",
            system_message=self.prompt,
            llm_config=self.llm_config["config_list"][0]
        )
        return assistant.assistant_id

    def process_message(self, message: str, context: Optional[str] = None, thread_id: Optional[str] = None) -> Tuple[str, str]:
        """
        Sends a message to the assistant and returns the reply and thread ID.

        Args:
            message (str): The user's input.
            context (str, optional): Optional context to enhance system message.
            thread_id (str, optional): Optional OpenAI thread ID to reuse.

        Returns:
            Tuple[str, str]: (assistant reply, thread_id used)
        """
        if not thread_id:
            thread = self.client.beta.threads.create()
            thread_id = thread.id

        system_prompt = self.prompt
        if context:
            system_prompt = f"Previously you were helping with this:\n{context}\n\nContinue helping in a natural way."

        self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message
        )

        run = self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=self.assistant_id,
            instructions=system_prompt
        )

        while True:
            run_status = self.client.beta.threads.runs.retrieve(
                thread_id=thread_id, run_id=run.id
            )
            if run_status.status == "completed":
                break

        messages = self.client.beta.threads.messages.list(thread_id=thread_id)
        assistant_reply = next(
            (msg for msg in messages.data if msg.role == "assistant"),
            None
        )

        reply = assistant_reply.content[0].text.value if assistant_reply else "❌ No response."
        return reply, thread_id

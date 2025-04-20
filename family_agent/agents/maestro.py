# File: autogen/agents/maestro.py

import os
from pathlib import Path
from dotenv import load_dotenv
import json

from autogen import AssistantAgent
from typing import Optional

class MasterAssistant:
    """
    MasterAssistant encapsulates the behavior and configuration of the main assistant agent.
    """

    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initializes the assistant using environment variables and configuration files.
        """
        self.base_path = config_dir or Path(__file__).resolve().parent.parent
        self._load_environment()
        self.prompt = self._load_prompt()
        self.llm_config = self._load_llm_config()
        self.agent = self._create_agent()

    def _load_environment(self) -> None:
        """
        Loads environment variables from .env file.
        """
        dotenv_path = self.base_path / ".env"
        load_dotenv(dotenv_path=dotenv_path)

    def _load_prompt(self) -> str:
        """
        Loads the assistant's prompt from file.
        """
        prompt_path = self.base_path / "configs" / "prompt_maestro.txt"
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()

    def _load_llm_config(self) -> dict:
        """
        Loads the LLM configuration from JSON and injects environment variables.
        """
        config_path = self.base_path / "configs" / "llm_config.json"
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        
        # Replace environment variables if any placeholders are present
        for entry in config.get("config_list", []):
            if "${OPENAI_API_KEY}" in entry.get("api_key", ""):
                entry["api_key"] = os.getenv("OPENAI_API_KEY")
        return config

    def _create_agent(self) -> AssistantAgent:
        """
        Creates and returns the AssistantAgent instance.
        """
        return AssistantAgent(
            name="Maestro",
            system_message=self.prompt,
            llm_config=self.llm_config["config_list"][0]
        )
    def process_message(self, message: str) -> str:
        """
        Processes a message and returns the assistant's response as string.
        """
        user_message = {
            "role": "user",
            "content": message
        }

        response = self.agent.generate_reply(messages=[user_message])

        # Some versions of pyautogen return a string directly
        if isinstance(response, str):
            return response

        # If not, try to extract content from a dict
        if isinstance(response, dict):
            return response.get("content", "No response generated.")

        return "Unsupported response format."

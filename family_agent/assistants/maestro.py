# File: family_agent/assistants/maestro.py

import os
import json
import time
import requests
from pathlib import Path
from typing import Optional, Tuple, List
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.beta.threads import Run


class MasterAssistant:
    """
    MasterAssistant handles all interactions with OpenAI's Assistants API (v2),
    including sending messages, managing threads, tool calls, and run lifecycle.
    """

    def __init__(self, config_dir: Optional[Path] = None) -> None:
        self.context_user = None
        self.base_path: Path = config_dir or Path(__file__).resolve().parent.parent
        self._load_environment()
        self.prompt: str = self._load_prompt()
        self.assistant_id: str = self._load_assistant_id()
        self.client: OpenAI = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            default_headers={"OpenAI-Beta": "assistants=v2"}
        )
        self._ensure_tools_are_registered()

    def _load_environment(self) -> None:
        dotenv_path = self.base_path / ".env"
        load_dotenv(dotenv_path=dotenv_path)

    def _load_prompt(self) -> str:
        prompt_path = self.base_path / "configs" / "prompt_maestro.txt"
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()

    def _load_assistant_id(self) -> str:
        tools_path = self.base_path / "configs" / "tools_config.json"
        with open(tools_path, "r", encoding="utf-8") as f:
            tools = json.load(f)

        assistant_id: Optional[str] = tools.get("maestro")
        if not assistant_id:
            raise ValueError("🛑 Assistant ID for 'maestro' not found in tools_config.json")

        return assistant_id

    def _ensure_tools_are_registered(self) -> None:
        """
        Ensures that the assistant has the required tools (e.g., crear_recordatorio).
        This step is idempotent.
        """
        self.client.beta.assistants.update(
            assistant_id=self.assistant_id,
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "crear_recordatorio",
                        "description": "Creates a reminder with a message and a specific time for the user.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "text": {"type": "string"},
                                "hour": {"type": "string"},
                                "user_id": {"type": "string"},
                                "channel": {"type": "string"},
                                "chat_id": {"type": "integer"}
                            },
                            "required": ["text", "hour", "user_id", "channel", "chat_id"]
                        }
                    }
                }
            ]
        )

    def process_message(
        self,
        message: str,
        context: Optional[str] = None,
        thread_id: Optional[str] = None
    ) -> Tuple[str, str]:
        """
        Sends a message to the assistant and handles responses, including tool calls and output submission.
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

        run: Run = self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=self.assistant_id,
            instructions=system_instructions
        )

        while True:
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )

            if run.status == "completed":
                break
            elif run.status == "requires_action" and run.required_action:
                self._handle_tool_calls(thread_id, run)
            elif run.status == "failed":
                return "❌ Assistant run failed.", thread_id

            time.sleep(1)

        messages = self.client.beta.threads.messages.list(thread_id=thread_id)
        assistant_reply = next(
            (msg for msg in messages.data if msg.role == "assistant"),
            None
        )

        reply = assistant_reply.content[0].text.value if assistant_reply else "❌ No response."
        return reply, thread_id

    def _handle_tool_calls(self, thread_id: str, run: Run) -> None:
        """
        Handles tool calls required by the assistant by executing the corresponding Azure Function.
        """
        tool_outputs = []

        for tool_call in run.required_action.submit_tool_outputs.tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            # Add user context
            arguments["user_id"] = str(self.context_user.id)
            arguments["chat_id"] = self.context_user.telegram_chat_id
            arguments["channel"] = "telegram"

            try:
                if function_name == "crear_recordatorio":
                    response_data = self._execute_reminder_tool(arguments)

                    output_str = (
                        str(response_data["message"]) if isinstance(response_data, dict) and "message" in response_data
                        else json.dumps(response_data) if isinstance(response_data, dict)
                        else str(response_data)
                    )

                    tool_outputs.append({
                        "tool_call_id": tool_call.id,
                        "output": output_str 
                    })


            except Exception as e:
                print(f"❌ Error executing tool {function_name}: {e}")
                tool_outputs.append({
                    "tool_call_id": tool_call.id,
                    "output": f"Tool '{function_name}' failed: {str(e)}"
                })

        print(f"✅ Output enviado: {output_str} (type: {type(output_str)})")

        self.client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread_id,
            run_id=run.id,
            tool_outputs=tool_outputs
        )

    def _execute_reminder_tool(self, params: dict) -> dict:
        """
        Executes the 'crear_recordatorio' Azure Function by sending an HTTP POST request.
        """
        azure_function_url = os.getenv("AZURE_REMINDER_FUNCTION_URL")

        try:
            response = requests.post(
                url=azure_function_url,
                json=params,
                timeout=10
            )
            return response.json()
        except Exception as e:
            return {
                "status": "error",
                "message": f"Tool execution failed: {str(e)}"
            }

    def _build_system_prompt(self, context: Optional[str]) -> str:
        """
        Builds the system prompt with optional context.
        """
        if not context:
            return self.prompt
        return f"Previously you were helping with this:\n{context}\n\nContinue helping in a natural way."

    def set_context_user(self, user) -> None:
        """
        Store user context to be used during tool call execution.
        """
        self.context_user = user

# File: autogen/flows/validate_config.py

import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Base project path
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
dotenv_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=dotenv_path)

# Load env values
api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("OPENAI_MODEL")
temperature = os.getenv("TEMPERATURE")

print("✅ Environment variables loaded:")
print(f"OPENAI_API_KEY: {'✔️' if api_key else '❌'}")
print(f"OPENAI_MODEL: {model}")
print(f"TEMPERATURE: {temperature}")

# Load llm_config
llm_config_path = BASE_DIR / "configs" / "llm_config.json"
try:
    with open(llm_config_path, "r", encoding="utf-8") as f:
        llm_config = json.load(f)
        print("\n✅ llm_config.json loaded:")
        print(json.dumps(llm_config, indent=2))
except FileNotFoundError:
    print(f"❌ File not found: {llm_config_path}")

# Load prompt
prompt_path = BASE_DIR / "configs" / "prompt_maestro.txt"
try:
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt = f.read()
        print("\n✅ prompt_maestro.txt loaded:")
        print(prompt[:200] + "...")
except FileNotFoundError:
    print(f"❌ File not found: {prompt_path}")

# Load tools config
tools_path = BASE_DIR / "configs" / "tools_config.json"
try:
    with open(tools_path, "r", encoding="utf-8") as f:
        tools = json.load(f)
        print("\n✅ tools_config.json loaded:")
        print(json.dumps(tools, indent=2))
except FileNotFoundError:
    print(f"❌ File not found: {tools_path}")

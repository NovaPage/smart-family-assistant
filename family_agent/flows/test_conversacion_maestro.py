import sys
from pathlib import Path

# Add autogen/ to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from agents.maestro import MasterAssistant

def test_master_assistant():
    assistant = MasterAssistant()
    message = "Hola, ¿qué puedo hacer para dormir mejor por las noches?"
    response = assistant.process_message(message)
    
    print("🗨️ Usuario:", message)
    print("🤖 Maestro:", response)

if __name__ == "__main__":
    test_master_assistant()

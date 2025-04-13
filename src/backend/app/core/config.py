import os
from dotenv import load_dotenv

def load_env():
    load_dotenv()
    print(f"Entorno cargado: {os.getenv('ENVIRONMENT', 'dev')}")

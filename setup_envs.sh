#!/bin/bash

# Archivo: setup_envs.sh
# Ubicación: asistente-familiar-inteligente/

echo "🐍 Inicializando entorno virtual para backend..."

cd src/backend
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install fastapi uvicorn pydantic python-dotenv openai
pip freeze > requirements.txt
deactivate
cd ../../

echo "✅ Entorno backend listo."

echo "🤖 Inicializando entorno virtual para autogen..."

cd autogen
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install openai autogen python-dotenv
pip freeze > requirements.txt
deactivate
cd ..

echo "✅ Entorno autogen listo."

echo "⚡ (Opcional) Entorno virtual para Azure Functions..."

cd azure
python -m venv .venv
source .venv/bin/activate
pip install azure-functions
pip freeze > requirements.txt
deactivate
cd ..

echo "✅ Setup de entornos completado 🎉"

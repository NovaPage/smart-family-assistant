#!/bin/bash

# Archivo: setup_envs.sh
# Ubicación: asistente-familiar-inteligente/

echo "🐍 Inicializando entorno virtual para backend..."

cd src/backend
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install fastapi uvicorn pydantic python-dotenv openai
deactivate
cd ../../

echo "✅ Entorno backend listo."

echo "🤖 Inicializando entorno virtual para autogen..."

cd autogen
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install openai autogen python-dotenv
deactivate
cd ..

echo "✅ Entorno autogen listo."

echo "⚡ (Opcional) Entorno virtual para Azure Functions..."

cd azure
python3 -m venv .venv
source .venv/bin/activate
pip install azure-functions
deactivate
cd ..

echo "✅ Setup de entornos completado 🎉"

#!/bin/bash

# Archivo: init_autogen.sh
# Ubicación: asistente-familiar-inteligente/

echo "🤖 Inicializando estructura de autogen..."

# Crear carpetas
mkdir -p autogen/{agents,tools,flows,configs}

# Crear entorno virtual
cd autogen
python -m venv .venv
source .venv/bin/activate

# Instalar dependencias base para desarrollo con Autogen
pip install --upgrade pip
pip install openai python-dotenv

# Congelar dependencias
pip freeze > requirements.txt

# Desactivar entorno virtual
deactivate
cd ..

echo "✅ Autogen configurado correctamente:"
echo "📁 Carpetas: agents/, tools/, flows/, configs/"
echo "🧪 Entorno virtual creado en autogen/.venv"
echo "📦 Dependencias registradas en autogen/requirements.txt"

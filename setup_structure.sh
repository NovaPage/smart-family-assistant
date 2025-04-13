#!/bin/bash

# Archivo: setup_structure.sh
# Ubicación: asistente-familiar-inteligente/

echo "📁 Creando estructura de carpetas..."

mkdir -p autogen/{agents,configs,tools,flows}
mkdir -p azure/.placeholder
mkdir -p src/backend/app/{api,services,models,core}
mkdir -p src/backend/tests
mkdir -p src/frontend

touch .env.template README.md

echo "✅ Estructura base creada."

#!/bin/bash

# Archivo: init_azure_function.sh
# Ubicación: asistente-familiar-inteligente/

FUNCTION_NAME="crear-recordatorio"
AZURE_DIR="azure/${FUNCTION_NAME}"

echo "⚡ Creando función Azure: ${FUNCTION_NAME}..."

# Crear estructura base
mkdir -p "${AZURE_DIR}"

# Crear __init__.py
cat > "${AZURE_DIR}/__init__.py" <<EOF
import logging
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Procesando recordatorio...')
    return func.HttpResponse("Recordatorio creado", status_code=200)
EOF

# Crear function.json
cat > "${AZURE_DIR}/function.json" <<EOF
{
  "scriptFile": "__init__.py",
  "bindings": [
    {
      "authLevel": "function",
      "type": "httpTrigger",
      "direction": "in",
      "name": "req",
      "methods": ["post"]
    },
    {
      "type": "http",
      "direction": "out",
      "name": "\$return"
    }
  ]
}
EOF

# Crear entorno virtual en azure/ si no existe
cd azure
if [ ! -d ".venv" ]; then
    echo "🧪 Creando entorno virtual para Azure Functions..."
    python -m venv .venv
fi

# Activar entorno y preparar requirements
source .venv/bin/activate
pip install --upgrade pip
pip install azure-functions
pip freeze > requirements.txt
deactivate
cd ..

echo "✅ Azure Function '${FUNCTION_NAME}' creada correctamente"
echo "🧪 Entorno virtual: azure/.venv"
echo "📦 Dependencias: azure/requirements.txt"

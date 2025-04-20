#!/bin/bash

# RUTA BASE
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ACTIVA EL ENTORNO VIRTUAL DEL BACKEND
BACKEND_VENV="$PROJECT_ROOT/src/backend/.venv"

if [ -f "$BACKEND_VENV/Scripts/activate" ]; then
    # Windows (Git Bash, MINGW)
    source "$BACKEND_VENV/Scripts/activate"
elif [ -f "$BACKEND_VENV/bin/activate" ]; then
    # Linux / macOS
    source "$BACKEND_VENV/bin/activate"
else
    echo "❌ No se encontró un entorno virtual válido en: $BACKEND_VENV"
    exit 1
fi

# AGREGA EL PROYECTO RAÍZ AL PYTHONPATH PARA QUE pueda usar autogen/
export PYTHONPATH="$PROJECT_ROOT"

# CAMBIA AL DIRECTORIO DEL BACKEND
cd "$PROJECT_ROOT/src/backend"

# INICIA EL SERVIDOR UVICORN
uvicorn app.main:app --reload

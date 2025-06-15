## 📘 `README.md` – Proyecto: Asistente Familiar Inteligente

# 🤖 Asistente Familiar Inteligente

Este proyecto implementa una arquitectura modular para un sistema de agentes inteligentes basado en Autogen, con backend en FastAPI, frontend en Angular, y herramientas serverless vía Azure Functions.

## 📦 Estructura General del Proyecto

```
asistente-familiar-inteligente/
├── autogen/         # Agentes, flujos, configuraciones e interfaces con tools
├── azure/           # Azure Functions expuestas como herramientas externas
├── src/
│   ├── backend/     # API REST en FastAPI, validaciones, conexión con agentes
│   └── frontend/    # SPA en Angular
```

---

## 🚀 Instrucciones para levantar cada módulo

### 1. Backend (FastAPI)

```bash
cd src/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

📌 **Versión recomendada de Python:** `3.13.x`

---

### 2. Autogen (Agentes inteligentes)

```bash
cd autogen
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

📌 **Versión recomendada de Python:** `3.13.x`

---

### 3. Frontend (Angular)

### Pending
---

### 4. Azure Functions (Tools externas)

```bash
cd azure
pyenv shell 3.10.5
pyenv exec python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
func start
```

📌 **Versión requerida de Python:** `3.10.5`

---

## 🔐 Variables de entorno por módulo

### 🌐 `src/backend/.env`

```env
ENVIRONMENT=dev
```

### 🤖 `autogen/.env`

```env
OPENAI_API_KEY=sk-...
ENVIRONMENT=dev
```

### ⚡ `azure/local.settings.json`

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python"
  }
}
```

> ⚠️ Todos los archivos `.env` y `local.settings.json` deben estar listados en `.gitignore`.

---

## ⚡ Cómo crear una nueva Azure Function

1. Ejecuta el siguiente script desde la raíz del proyecto:

```bash
./init_azure_function.sh
```

2. Esto crea:

```
azure/nueva-funcion/
├── __init__.py
├── function.json
```

3. Luego entra a la carpeta `azure`, activa el entorno virtual y actualiza:

```bash
cd azure
source .venv/bin/activate
pip install -r requirements.txt
func start
```

---

## 📎 Recomendaciones

- Usa `pyenv` para controlar versiones específicas de Python.
- Mantén los entornos virtuales separados por módulo.
- Usa `pip freeze > requirements.txt` después de cada cambio de dependencias.
- Usa `curl` o Postman para probar endpoints y funciones.

---
## 📅 Última actualización

Abril 2025

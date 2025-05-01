import logging
import azure.functions as func
from models.reminder import Reminder
from repositories.reminder_repository import ReminderRepository
from utils.env import get_env_var
from datetime import datetime

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("⏰ Crear Recordatorio triggered.")

    try:
        data = req.get_json()

        required_fields = ["text", "hour", "user_id", "chat_id", "channel"]
        if not all(field in data for field in required_fields):
            return func.HttpResponse("Missing fields", status_code=400)

        reminder = Reminder(
            text=data["text"],
            hour=data["hour"],
            user_id=data["user_id"],
            chat_id=data["chat_id"],
            channel=data["channel"],
            status="pending",
            created_at=datetime.utcnow()
        )

        repo = ReminderRepository()
        repo.save(reminder)

        logging.info(f"✅ Recordatorio guardado: {reminder.text}")
        return func.HttpResponse("Recordatorio creado correctamente", status_code=200)

    except Exception as e:
        logging.error(f"❌ Error en crear-recordatorio: {str(e)}")
        return func.HttpResponse(f"Error interno: {str(e)}", status_code=500)

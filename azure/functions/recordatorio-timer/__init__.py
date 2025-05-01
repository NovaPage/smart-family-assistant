# File: azure/functions/recordatorio-timer/__init__.py

import logging
from datetime import datetime, timedelta, timezone

import azure.functions as func

from app.repositories import reminder_repository
from app.services.telegram_service import telegram_service


def main(mytimer: func.TimerRequest) -> None:
    """
    Timer-triggered function to check and send pending reminders every minute.
    """
    logging.info("🔔 Reminder timer triggered at %s", datetime.utcnow().isoformat())

    now_utc: datetime = datetime.utcnow().replace(second=0, microsecond=0)
    reminders = reminder_repository.get_pending_reminders_at(now_utc)

    if not reminders:
        logging.info("✅ No pending reminders at this time.")
        return

    for reminder in reminders:
        try:
            if reminder.channel == "telegram" and reminder.chat_id:
                telegram_service.send_reminder(
                    chat_id=reminder.chat_id,
                    message=reminder.text
                )
                reminder_repository.mark_as_sent(reminder.id)
                logging.info("📨 Reminder sent to user %s", reminder.user_id)
            else:
                logging.warning("⚠️ Unsupported channel or missing chat_id for reminder %s", reminder.id)

        except Exception as e:
            logging.error("❌ Failed to send reminder %s: %s", reminder.id, str(e))

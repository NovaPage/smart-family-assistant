# File: src/backend/app/repositories/reminder_repository.py

from datetime import datetime
from uuid import UUID
from typing import List

from azure.cosmos import exceptions

from app.models.reminder import Reminder, ReminderStatus
from app.repositories.cosmos_client import database

reminders_container = database.get_container_client("reminders")


def save_reminder(reminder: Reminder) -> None:
    """
    Saves a new reminder into the Cosmos DB container.
    """
    reminders_container.create_item(reminder.model_dump(mode="json"))


def get_pending_reminders_at(target_datetime: datetime) -> List[Reminder]:
    """
    Retrieves all pending reminders scheduled exactly at the given UTC minute.
    """
    query = """
    SELECT * FROM reminders r
    WHERE r.reminder_date = @target_datetime AND r.status = @status
    """
    params = [
        {"name": "@target_datetime", "value": target_datetime.isoformat()},
        {"name": "@status", "value": ReminderStatus.PENDING}
    ]
    items = reminders_container.query_items(query, parameters=params, enable_cross_partition_query=True)

    return [
        Reminder.model_validate(item)
        for item in items
    ]


def mark_as_sent(reminder_id: str) -> None:
    """
    Marks a reminder as sent by updating its status and sent_at timestamp.
    """
    try:
        reminder_doc = reminders_container.read_item(item=reminder_id, partition_key=reminder_id)
        reminder_doc["status"] = ReminderStatus.SENT
        reminder_doc["sent_at"] = datetime.utcnow().isoformat()

        reminders_container.replace_item(item=reminder_id, body=reminder_doc)
    except exceptions.CosmosResourceNotFoundError:
        print(f"⚠️ Reminder with ID {reminder_id} not found.")

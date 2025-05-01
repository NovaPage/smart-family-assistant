from db.cosmos_client import get_cosmos_client
from models.reminder import Reminder
from datetime import datetime

class ReminderRepository:
    def __init__(self):
        self.client, self.database = get_cosmos_client()
        self.container = self.database.get_container_client("reminders")

    def save(self, reminder: Reminder) -> None:
        document = reminder.dict()
        document["id"] = f"{reminder.user_id}-{reminder.created_at.isoformat()}"
        document["created_at"] = reminder.created_at.isoformat()
        self.container.create_item(body=document)

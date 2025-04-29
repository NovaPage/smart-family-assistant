# File: src/backend/app/repositories/thread_repository.py

from typing import Optional
from datetime import datetime, timedelta
from app.models.thread import ThreadInDB, ThreadCreate, ThreadStatus
from app.repositories.cosmos_client import database
from app.core.config import settings

_threads = database.get_container_client("threads")

def get_active_thread(user_id: str, source: str) -> Optional[ThreadInDB]:
    query = """
    SELECT * FROM threads t
    WHERE t.user_id = @user_id AND t.source = @source AND t.status = @status
    ORDER BY t.updated_at DESC
    """
    params = [
        {"name": "@user_id", "value": str(user_id)},
        {"name": "@source", "value": source},
        {"name": "@status", "value": ThreadStatus.OPEN}
    ]
    results = _threads.query_items(query, parameters=params, enable_cross_partition_query=True)
    first_result = next(iter(results), None)
    return ThreadInDB.model_validate(first_result) if first_result else None

def create_thread(data: ThreadCreate) -> ThreadInDB:
    new_thread = ThreadInDB(
        id=data.openai_thread_id,
        user_id=data.user_id,
        source=data.source,
        summary=data.summary,
        openai_thread_id=data.openai_thread_id
    )
    _threads.create_item(new_thread.model_dump(mode="json"))
    return new_thread

def close_thread(thread_id: str) -> None:
    thread_doc = _threads.read_item(item=thread_id, partition_key=thread_id)
    if not thread_doc:
        return
    thread_doc["status"] = ThreadStatus.CLOSED
    thread_doc["updated_at"] = datetime.utcnow().isoformat()
    _threads.replace_item(item=thread_id, body=thread_doc)

def get_last_closed_thread(user_id: str, source: str) -> Optional[ThreadInDB]:
    query = """
    SELECT * FROM threads t
    WHERE t.user_id = @user_id AND t.source = @source AND t.status = @status
    ORDER BY t.updated_at DESC
    """
    params = [
        {"name": "@user_id", "value": str(user_id)},
        {"name": "@source", "value": source},
        {"name": "@status", "value": ThreadStatus.CLOSED}
    ]
    results = _threads.query_items(query, parameters=params, enable_cross_partition_query=True)
    first_result = next(iter(results), None)
    return ThreadInDB.model_validate(first_result) if first_result else None

def is_thread_inactive(thread: ThreadInDB) -> bool:
    inactivity_duration = timedelta(minutes=settings.thread_inactivity_minutes)
    return (datetime.utcnow() - thread.updated_at) > inactivity_duration

def update_timestamp(openai_thread_id: str) -> None:
    query = f"SELECT * FROM c WHERE c.openai_thread_id = '{openai_thread_id}'"
    items = list(_threads.query_items(query=query, enable_cross_partition_query=True))

    if not items:
        return

    thread_doc = items[0]
    thread_doc["updated_at"] = datetime.utcnow().isoformat()

    _threads.replace_item(item=thread_doc["id"], body=thread_doc)

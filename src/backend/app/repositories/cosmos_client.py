# File: src/backend/app/repositories/cosmos_client.py

from azure.cosmos import CosmosClient
from app.core.config import settings

# Shared Cosmos DB client for reuse
cosmos_client = CosmosClient(settings.cosmos_db_uri, credential=settings.cosmos_db_key)
database = cosmos_client.get_database_client(settings.cosmos_db_database)

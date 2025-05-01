import os
from azure.cosmos import CosmosClient
from utils.env import get_env_var

def get_cosmos_client():
    url = get_env_var("COSMOSDB_URL")
    key = get_env_var("COSMOSDB_KEY")
    db_name = get_env_var("COSMOSDB_DATABASE_NAME")

    client = CosmosClient(url, credential=key)
    database = client.get_database_client(db_name)
    return client, database

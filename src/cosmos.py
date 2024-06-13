import json
import os
from ulid import ULID
from azure.cosmos import CosmosClient

credential = os.environ["AZURE_COSMOS_CREDENTIALS"]
endpoint = os.environ["AZURE_COSMOSDB_ENDPOINT"]
client = CosmosClient(url=endpoint, credential=credential)


def get_generate_history():
    database = client.get_database_client("FismApp")
    container = database.get_container_client("Appinout")

    query_text = "SELECT * FROM Appinout WHERE Appinout.input like '%sample%'"
    results = container.query_items(
        query=query_text,
        parameters=[],
        enable_cross_partition_query=True,
    )
    items = [item for item in results]
    return json.dumps(items, indent=True)


def write_generate_history(input, output):
    database = client.get_database_client("FismApp")
    container = database.get_container_client("Appinout")

    id = ULID()
    new_item = {
        "id": str(id),
        "input": input,
        "output": output,
    }
    return container.upsert_item(new_item)


if __name__ == "__main__":
    print(write_generate_history("sample input", "sample output"))
    print(get_generate_history())
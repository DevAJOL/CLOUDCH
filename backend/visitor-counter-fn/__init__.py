import logging
import json
import os
from azure.cosmos import CosmosClient, PartitionKey
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    cosmos_db_endpoint = os.getenv('COSMOS_DB_ENDPOINT') #"https://visitor-counter.documents.azure.com:443/"
    cosmos_db_key = os.getenv('COSMOS_DB_KEY') #"1SO7XbJhJ4MnfZF3k2eTVIk2xo7XSA2tWVWvHYk2VkKo1imvmG2ZHDovcBLdpHr9tFSOjvkn2u1AACDboROMyA=="
    database_name = 'visitor-counter-db'
    container_name = 'visitor-counter-container'

    client = CosmosClient(cosmos_db_endpoint, cosmos_db_key)
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)
    logging.info(database)
    # assuming your items have a 'visitors' field
    for item in container.query_items(
        query='SELECT * FROM c WHERE c.id = "visitorCount"',
        enable_cross_partition_query=True):
        if 'visitors' in item:
            item['visitors'] += 1
        else:
            # If 'visitors' key doesn't exist, initialize it
            item['visitors'] = 1
        container.upsert_item(item)

    response_data = {"message": "Visitor count updated.",
    "status_code": 200,
    "count": item['visitors']} # Use 'item['visitors']' to get the count from CosmosDB
    response_json = json.dumps(response_data)
    logging.info(f'Response JSON: {response_json}')  # Log the response data


    return func.HttpResponse(response_json, status_code=200)

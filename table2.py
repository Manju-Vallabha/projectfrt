from azure.data.tables import TableServiceClient
from dotenv import load_dotenv
import os
import pandas as pd
import datetime


connection_string = "DefaultEndpointsProtocol=https;AccountName=informationdetails;AccountKey=BDRNISM6nfXnxCEmqw0qc8OwVsEbVaFsHiRPU6BDyAdwOEeewbIg4PzKqo9wgBBBC34K5RmA853XACDbYea5dw==;EndpointSuffix=cosmos.azure.com"
table_service_client = TableServiceClient.from_connection_string(conn_str=connection_string)
# Get a TableClient for the specific table
table_client = table_service_client.get_table_client("informationdetails")



def entity_update(username,response):
    entity = {
        'PartitionKey': username,
        'RowKey': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        'Symptoms': response}
    table_client.create_entity(entity=entity)
    return "Success"


def entity_retrieve(partition_key):
    query_filter = f"PartitionKey eq '{partition_key}'"
    entities = table_client.query_entities(query_filter=query_filter)

    # Convert the entities to a DataFrame
    data = []
    for entity in entities:
        # Ensure that the entity has both 'RowKey' and 'severity'
        date_str = entity.get('RowKey')
        severity = entity.get('Symptoms')
        if date_str and severity:
            # Attempt to parse the date string with the expected format

                date = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                # Append only the date part (without time)
                data.append({
                    'date': date.date(),  # Extract date part only
                    'severity': severity
                })
    print(data)

    if data:
        return data
    
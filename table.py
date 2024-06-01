from azure.data.tables import TableServiceClient
from dotenv import load_dotenv
import os
import pandas as pd
import datetime


connection_string = "DefaultEndpointsProtocol=https;AccountName=astmatracker;AccountKey=hzaPyxWgcRe5VjwCBgmhICqI5CIfq1iJgO7idqBZ7bvsWwul2akCJ8bxdy7AN6CwTFU9glkuZnGnACDbY2CZcQ==;EndpointSuffix=cosmos.azure.com"
table_service_client = TableServiceClient.from_connection_string(conn_str=connection_string)
# Get a TableClient for the specific table
table_client = table_service_client.get_table_client("userdetails")



def entity_update(username,age,gender):
    entity = {
        'PartitionKey': username,
        'RowKey': str(datetime.datetime.now()),
        'Age': age,
        'Gender': gender  }
    table_client.create_entity(entity=entity)
    return "Success"

def entity_retrieve(partition_key):
    query_filter = f"PartitionKey eq '{partition_key}'"
    entities = table_client.query_entities(query_filter)
    for entity in entities:
        age = entity.get('Age')
        gender = entity.get('Gender')
        return age, gender

    
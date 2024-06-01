
from azure.ai.ml import MLClient
from azure.identity import ClientSecretCredential
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get Azure credentials from environment variables
client_id = os.getenv("AZURE_CLIENT_ID")
tenant_id = os.getenv("AZURE_TENANT_ID")
client_secret = os.getenv("AZURE_CLIENT_SECRET")
subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
resource_group = os.getenv("AZURE_RESOURCE_GROUP")
workspace_name = os.getenv("AZURE_WORKSPACE_NAME")
endpoint_name = os.getenv("AZURE_ENDPOINT_NAME")
deployment_name = os.getenv("AZURE_DEPLOYMENT_NAME")

def invoke_endpoint():
    try:
        # Initialize MLClient with ClientSecretCredential
        credential = ClientSecretCredential(tenant_id, client_id, client_secret)
        ml_client = MLClient(credential, subscription_id, resource_group, workspace_name)

        # Save request JSON to a file


        # Invoke the endpoint
        response = ml_client.online_endpoints.invoke(
            endpoint_name=endpoint_name,
            deployment_name=deployment_name,
            request_file="input.json",
        )

        return response
    except Exception as e:
        return str(e)

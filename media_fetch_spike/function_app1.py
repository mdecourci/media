import json
import os
import traceback

import azure.functions as func
from azure.storage.blob import BlobServiceClient

app = func.FunctionApp()
AZURE_STORAGE_CONTAINER_NAME = "container-spikeblob-test"
BLOB_NAME = "output/reports/example.txt"

@app.route(route="blob", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def test_blob(req: func.HttpRequest) -> func.HttpResponse:

    try:
        content = "Data content to save to blob"

        blob_service_account = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
        container_name = AZURE_STORAGE_CONTAINER_NAME

        blob_client = blob_service_account.get_blob_client(container=container_name, blob=BLOB_NAME)

        blob_client.upload_blob(data=content, overwrite=True)

        return func.HttpResponse(
            f"Successfully wrote {BLOB_NAME} to {container_name}",
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        error_details = traceback.format_exc()

        return func.HttpResponse(
            body=(
                f"FAILED\n\n"
                f"Error: {str(e)}\n\n"
                f"Stack trace:\n{error_details}"
            ),
            status_code=200
        )



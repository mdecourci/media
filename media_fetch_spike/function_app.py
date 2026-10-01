import json
import azure.functions as func

app = func.FunctionApp()

@app.route(route="hello", methods=["POST"])
@app.queue_output(
    arg_name="outputQueue",
    queue_name="media-processing",
    connection="AzureWebJobsStorage"
)
def hello_world(
    req: func.HttpRequest,
    outputQueue: func.Out[str]
) -> func.HttpResponse:

    message = {
        "event_type": "media.fetch.completed",
        "document_id": "example-123",
        "status": "completed"
    }

    outputQueue.set(json.dumps(message))

    return func.HttpResponse(
        "Message written to media-processing queue",
        status_code=200
    )
import json
import azure.functions as func

app = func.FunctionApp()

@app.route(route="hello", methods=["POST"])
def hello_world(req: func.HttpRequest) -> func.HttpResponse:
    name = req.get_json().get("name", "World")

    return func.HttpResponse(
        json.dumps({"message": f"Hello, {name}!"}),
        mimetype="application/json",
        status_code=200
    )

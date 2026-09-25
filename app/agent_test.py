"""
AI summarization agent - Azure Foundry "instant access" (preview), API-key auth,
NO deployment step required

Calls any supported model by name directly - no Model catalog deployment needed.
Uses a plain API key against the project's /openai/v1 route (no azure-identity,
no AIProjectClient, no DefaultAzureCredential).

PREVIEW CAVEATS
-----------------
- Currently guaranteed only in the West US 3 region.
- No SLA - fine for experimentation, not yet something to depend on in production.
- The set of instantly-callable models changes over time; check the Foundry
  portal's model catalog (filter: "Instant" under Deployment options) for the
  current list.

SETUP (Foundry portal - https://ai.azure.com)
--------------------------------------------------------------------------
1. Create/confirm a project in West US 3 (required during preview).
2. Skip the Model catalog "Deploy" step entirely - nothing to deploy.
3. Project Overview page -> copy the project endpoint, e.g.:
   https://<resource-name>.services.ai.azure.com/api/projects/<project-name>
4. Resource's "Keys and Endpoint" page -> copy an API key.

ENVIRONMENT VARIABLES (PyCharm: Run -> Edit Configurations -> Environment variables)
--------------------------------------------------------------------------
   AZURE_AI_PROJECT_ENDPOINT=https://<resource-name>.services.ai.azure.com/api/projects/<project-name>
   AZURE_OPENAI_API_KEY=<your key>

pip install openai
"""

import json
import os

from openai import OpenAI

# Any instant-access model name works here directly - no deployment required.
# Check the Foundry model catalog ("Instant" filter) for the current list.
AVAILABLE_MODELS = [
    "gpt-5-nano",
    "gpt-5-mini",
    "gpt-4.1-nano",
]

MODEL_NAME = AVAILABLE_MODELS[0]  # change this line to switch models


def get_client() -> OpenAI:
    project_endpoint = os.environ.get("AZURE_AI_PROJECT_ENDPOINT")
    api_key = os.environ.get("AZURE_OPENAI_API_KEY")
    if not project_endpoint or not api_key:
        raise RuntimeError(
            "Set AZURE_AI_PROJECT_ENDPOINT and AZURE_OPENAI_API_KEY as "
            "environment variables. The project endpoint is on the project's "
            "Overview page; the API key is on the resource's Keys and Endpoint page."
        )
    # This is exactly what AIProjectClient.get_openai_client() builds internally
    # (project endpoint + "/openai/v1"), just constructed directly so a plain
    # API key can be used instead of azure-identity/DefaultAzureCredential.
    base_url = f"{project_endpoint.rstrip('/')}/openai/v1"
    return OpenAI(api_key=api_key, base_url=base_url)


# ---------------------------------------------------------------------------
# Tool functions - ordinary Python functions the model can choose to call.
# ---------------------------------------------------------------------------

def get_word_count(text: str) -> dict:
    """Return the word count of a piece of text."""
    return {"word_count": len(text.split())}


def flag_priority(sector: str) -> dict:
    """Look up whether a given sector is high priority for reporting."""
    high_priority_sectors = {"network_operator", "generator"}
    return {"sector": sector, "high_priority": sector in high_priority_sectors}


AVAILABLE_TOOLS = {
    "get_word_count": get_word_count,
    "flag_priority": flag_priority,
}

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "get_word_count",
            "description": "Count the number of words in a piece of text.",
            "parameters": {
                "type": "object",
                "properties": {"text": {"type": "string"}},
                "required": ["text"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "flag_priority",
            "description": "Check whether a given sector is high priority for reporting.",
            "parameters": {
                "type": "object",
                "properties": {"sector": {"type": "string"}},
                "required": ["sector"],
            },
        },
    },
]


def summarize_with_tools(text: str, sector: str, model: str = MODEL_NAME) -> str:
    """Summarise `text`, letting the model call tools if it decides they'd help."""
    client = get_client()

    messages = [
        {
            "role": "system",
            "content": (
                "You are a concise summarization assistant. Summarise the given "
                "text in 2-3 sentences, in neutral, factual language. Use the "
                "available tools if they would help produce a better-informed "
                "summary."
            ),
        },
        {"role": "user", "content": f"Sector: {sector}\n\nText:\n{text}"},
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=TOOLS_SCHEMA,
        tool_choice="auto",
        temperature=0.2,
        max_tokens=300,
    )
    message = response.choices[0].message

    while message.tool_calls:
        messages.append(message)
        for tool_call in message.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments)
            result = AVAILABLE_TOOLS[func_name](**func_args)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result),
                }
            )

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=TOOLS_SCHEMA,
            tool_choice="auto",
            temperature=0.2,
            max_tokens=300,
        )
        message = response.choices[0].message

    return message.content


if __name__ == "__main__":
    sample_text = (
        "SSEN announced grid upgrades intended to speed up the connection "
        "queue for Scottish renewable projects, following pressure from "
        "developers over multi-year delays."
    )

    # Experiment loop: run the same input through every candidate model,
    # with zero deployment step behind any of them.
    for model_name in AVAILABLE_MODELS:
        print(f"\n--- {model_name} ---")
        print(summarize_with_tools(sample_text, sector="network_operator", model=model_name))
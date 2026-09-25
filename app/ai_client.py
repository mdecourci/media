import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from functools import wraps
from typing import Any, Callable

from dotenv import load_dotenv
from openai import OpenAI


# ============================================================
# Configuration
# ============================================================

load_dotenv()


def required_env(name: str) -> str:
    """Return a required environment variable."""

    value = os.getenv(name)

    if not value:
        raise RuntimeError(
            f"Environment variable '{name}' has not been configured."
        )

    return value


PROJECT_ENDPOINT = required_env(
    "AZURE_AI_PROJECT_ENDPOINT"
)

API_KEY = required_env(
    "AZURE_AI_API_KEY"
)

MODEL = os.getenv(
    "FOUNDRY_MODEL",
    "gpt-5-mini",
)


# ============================================================
# OpenAI client connected to Microsoft Foundry
# ============================================================

client = OpenAI(
    base_url=f"{PROJECT_ENDPOINT}/openai/v1",
    api_key=API_KEY,
)


# ============================================================
# Tool infrastructure
# ============================================================

@dataclass
class RegisteredTool:
    """Information about a Python tool."""

    name: str
    description: str
    function: Callable[..., Any]
    parameters: dict[str, Any]


TOOLS: dict[str, RegisteredTool] = {}


def tool(
    name: str,
    description: str,
    parameters: dict[str, Any],
):
    """
    Register a Python function as an AI tool.

    The decorator:
      1. Registers the Python function.
      2. Creates the JSON schema used by the model.
    """

    def decorator(
        function: Callable[..., Any],
    ) -> Callable[..., Any]:

        registered_tool = RegisteredTool(
            name=name,
            description=description,
            function=function,
            parameters=parameters,
        )

        TOOLS[name] = registered_tool

        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return function(*args, **kwargs)

        return wrapper

    return decorator


# ============================================================
# Tools
# ============================================================

@tool(
    name="get_current_utc_time",
    description="Return the current UTC date and time.",
    parameters={
        "type": "object",
        "properties": {},
        "required": [],
        "additionalProperties": False,
    },
)
def get_current_utc_time() -> str:
    """
    Return the current UTC time.

    This is deliberately a simple tool to demonstrate
    function/tool calling.
    """

    return datetime.now(timezone.utc).isoformat()


@tool(
    name="get_article_statistics",
    description=(
        "Calculate basic statistics for an article, "
        "including character count, word count and "
        "sentence count."
    ),
    parameters={
        "type": "object",
        "properties": {
            "article": {
                "type": "string",
                "description": "The article text.",
            }
        },
        "required": ["article"],
        "additionalProperties": False,
    },
)
def get_article_statistics(article: str) -> dict[str, int]:
    """Calculate basic article statistics."""

    words = article.split()

    sentences = [
        sentence
        for sentence in article.replace("!", ".")
        .replace("?", ".")
        .split(".")
        if sentence.strip()
    ]

    return {
        "characters": len(article),
        "words": len(words),
        "sentences": len(sentences),
    }


# ============================================================
# Convert registered Python tools into Responses API tools
# ============================================================

def build_tools() -> list[dict[str, Any]]:
    """Build the tool definitions sent to the model."""

    result: list[dict[str, Any]] = []

    for registered_tool in TOOLS.values():

        result.append(
            {
                "type": "function",
                "name": registered_tool.name,
                "description": registered_tool.description,
                "parameters": registered_tool.parameters,
            }
        )

    return result


# ============================================================
# System prompt
# ============================================================

SYSTEM_PROMPT = """
You are the NESO Media Intelligence Agent.

Your job is to analyse news articles relating to:

- energy
- electricity
- gas
- renewables
- energy markets
- energy infrastructure
- energy policy
- National Energy System Operator (NESO)
- Great Britain's energy system
- organisations that influence or participate in the energy system
- data and artificial intelligence within the energy sector

You must be factual and objective.

Do not invent information.

Only make claims that can be supported by the supplied article.

If information is not available in the article, say that it
is not stated.

When analysing an article:

1. Identify the main subject.
2. Identify the important organisations.
3. Identify important people if they are mentioned.
4. Identify the main energy-sector issues.
5. Identify potential implications for NESO.
6. Produce a concise professional summary.
7. Identify important facts that may be useful for human review.

Use tools when they provide useful factual information.

You have access to Python functions through the tool interface.
Do not claim that you used a tool unless you actually used it.

Your response should be suitable for a professional media-intelligence
workflow.
"""


# ============================================================
# User prompt
# ============================================================

def build_user_prompt(article: str) -> str:
    """
    Build the user message.

    The article is supplied as user content rather than being
    embedded into the system prompt.
    """

    return f"""
Analyse the following news article.

Return:

- Title / subject
- Concise summary
- Key organisations
- Key people
- Energy-sector topics
- Relevance to NESO
- Important facts for human review

Article:

{article}
"""


# ============================================================
# Tool execution
# ============================================================

def execute_tool(
    tool_name: str,
    arguments: str,
) -> str:
    """
    Execute a Python tool requested by the model.
    """

    registered_tool = TOOLS.get(tool_name)

    if registered_tool is None:
        return json.dumps(
            {
                "error": (
                    f"Unknown tool: {tool_name}"
                )
            }
        )

    try:
        parsed_arguments = json.loads(arguments)

        result = registered_tool.function(
            **parsed_arguments
        )

        return json.dumps(
            result,
            ensure_ascii=False,
        )

    except Exception as exc:
        return json.dumps(
            {
                "error": str(exc)
            }
        )


# ============================================================
# Agent
# ============================================================

def run_agent(article: str) -> str:
    """
    Run the NESO Media Intelligence agent.

    The agent can:
      - receive a system prompt
      - receive a user prompt
      - call Python tools
      - receive tool results
      - continue reasoning
      - return the final response
    """

    user_prompt = build_user_prompt(article)

    tools = build_tools()

    response = client.responses.create(
        model=MODEL,

        # System-level instructions
        instructions=SYSTEM_PROMPT,

        # User-level input
        input=user_prompt,

        # Python tools exposed to the model
        tools=tools,

        # Keep tool execution simple and predictable
        parallel_tool_calls=False,
    )

    # --------------------------------------------------------
    # Tool-calling loop
    # --------------------------------------------------------

    while True:

        tool_calls = [
            item
            for item in response.output
            if item.type == "function_call"
        ]

        # No tool calls means the model has finished.
        if not tool_calls:
            return response.output_text.strip()

        # Build the tool outputs.
        tool_outputs: list[dict[str, Any]] = []

        for tool_call in tool_calls:

            print(
                f"Tool requested: "
                f"{tool_call.name}"
            )

            print(
                f"Arguments: "
                f"{tool_call.arguments}"
            )

            result = execute_tool(
                tool_name=tool_call.name,
                arguments=tool_call.arguments,
            )

            print(
                f"Tool result: {result}"
            )
            print()

            tool_outputs.append(
                {
                    "type": "function_call_output",
                    "call_id": tool_call.call_id,
                    "output": result,
                }
            )

        # Send the tool results back to the model.
        response = client.responses.create(
            model=MODEL,

            instructions=SYSTEM_PROMPT,

            input=tool_outputs,

            tools=tools,

            parallel_tool_calls=False,

            # Continue from the previous response.
            previous_response_id=response.id,
        )


# ============================================================
# Example article
# ============================================================

ARTICLE = """
The UK's energy system is undergoing significant change as
renewable generation increases and the electricity network
needs to accommodate new sources of low-carbon power.

National Energy System Operator is working with industry
stakeholders to improve the way energy-system data is shared
and used to support planning and real-time operations.

The organisation said that better access to data could help
energy companies and system planners understand changes in
demand and generation more effectively.
"""


# ============================================================
# Main
# ============================================================

def main() -> None:
    """Application entry point."""

    print()
    print("=" * 60)
    print("NESO MEDIA INTELLIGENCE AGENT")
    print("=" * 60)
    print()

    print(
        f"Foundry project: {PROJECT_ENDPOINT}"
    )

    print(
        f"Model: {MODEL}"
    )

    print(
        f"Registered tools: {len(TOOLS)}"
    )

    for tool_name in TOOLS:
        print(f"  - {tool_name}")

    print()
    print("Sending article to Foundry...")
    print()

    try:

        result = run_agent(
            ARTICLE
        )

        print()
        print("=" * 60)
        print("AGENT RESPONSE")
        print("=" * 60)
        print()
        print(result)
        print()

    except Exception as exc:

        print()
        print("=" * 60)
        print("ERROR")
        print("=" * 60)
        print()
        print(type(exc).__name__)
        print(str(exc))
        print()

        raise


if __name__ == "__main__":
    main()
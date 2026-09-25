import os

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient


def get_environment_variable(name: str) -> str:
    """Read a required environment variable."""
    value = os.getenv(name)

    if not value:
        raise RuntimeError(
            f"Environment variable '{name}' has not been configured."
        )

    return value


def create_client() -> tuple[AIProjectClient, object]:
    """Create the Microsoft Foundry project and OpenAI clients."""

    project_endpoint = get_environment_variable(
        "AZURE_AI_PROJECT_ENDPOINT"
    )

    credential = DefaultAzureCredential()

    project_client = AIProjectClient(
        endpoint=project_endpoint,
        credential=credential,
    )

    openai_client = project_client.get_openai_client()

    return project_client, openai_client


def generate_summary(
    openai_client: object,
    article: str,
) -> str:
    """Send an article to the Foundry model and return a summary."""

    model = os.getenv(
        "FOUNDRY_MODEL",
        "gpt-5-mini",
    )

    prompt = f"""
You are an AI news summarisation agent for NESO.

Summarise the following article.

Requirements:
- Produce a concise factual summary.
- Identify the main topic.
- Identify the organisations mentioned.
- Identify any important energy-sector implications.
- Do not invent information.
- Do not include information that is not supported by the article.
- Use clear professional English.

Article:

{article}
"""

    response = openai_client.responses.create(
        model=model,
        input=prompt,
        max_output_tokens=1000,
    )

    result = response.output_text

    if not result or not result.strip():
        raise RuntimeError(
            "The model returned an empty response."
        )

    return result.strip()


def main() -> None:
    """Application entry point."""

    print("Starting NESO Media AI Agent...")

    project_client, openai_client = create_client()

    print("Connected to Microsoft Foundry.")
    print(
        f"Using model: "
        f"{os.getenv('FOUNDRY_MODEL', 'gpt-5-mini')}"
    )

    article = """
    The UK's energy system is undergoing significant change as
    renewable generation increases and the electricity network
    needs to accommodate new sources of low-carbon power.

    National Energy System Operator is working with industry
    stakeholders to improve the way energy-system data is shared
    and used to support planning and real-time operations.
    """

    print("\nGenerating summary...\n")

    summary = generate_summary(
        openai_client,
        article,
    )

    print("----- SUMMARY -----")
    print(summary)
    print("-------------------")


if __name__ == "__main__":
    main()

import vertexai
from vertexai.preview import reasoning_engines
import os

# Retrieve environment variables
PROJECT_ID = os.environ.get("PROJECT_ID")
LOCATION = os.environ.get("LOCATION")
STAGING_BUCKET = os.environ.get("STAGING_BUCKET")

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket=STAGING_BUCKET,
)

def get_exchange_rate(
    currency_from: str = "USD",
    currency_to: str = "EUR",
    currency_date: str = "latest",
):
    """Retrieves the exchange rate between two currencies on a specified date.

    Uses the Frankfurter API (https://api.frankfurter.app/) to obtain exchange rate data.

    Args:
        currency_from: The base currency (3-letter currency code). Defaults to "USD" (US Dollar).
        currency_to: The target currency (3-letter currency code). Defaults to "EUR" (Euro).
        currency_date: The date for which to retrieve the exchange rate. Defaults to "latest" for the most recent exchange rate data. Can be specified in YYYY-MM-DD format for historical rates.

    Returns:
        dict: A dictionary containing the exchange rate information.
             Example: {"amount": 1.0, "base": "USD", "date": "2023-11-24", "rates": {"EUR": 0.95534}}
    """
    import requests
    response = requests.get(
        f"https://api.frankfurter.app/{currency_date}",
        params={"from": currency_from, "to": currency_to},
    )
    return response.json()

def create_agent():
    return reasoning_engines.LangchainAgent(
        model="gemini-1.0-pro-001",
        tools=[get_exchange_rate],
    )

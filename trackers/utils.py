import requests
from django.conf import settings

BASE_URL = "https://admin.kineticafricapp.com/"
EXTERNAL_API_TIMEOUT = 10  # optional
HEADER_KEY = {"x-secret-key": "rbAZcgfSXQLiHHCzYk8pDU9svNpnoFNZ"}


def call_custom_api_request(endpoint, params=None):
    """
    This is a utility function to make an external API call
    """

    url = f"{BASE_URL}/{endpoint}/"

    try:
        response = requests.get(
            url,
            headers=HEADER_KEY,
            params=params,
            timeout=EXTERNAL_API_TIMEOUT,
            verify=False,  # Optional, but often good to verify SSL in production
        )
        # Check if the request was successful
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

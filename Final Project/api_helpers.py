import os
import requests
from urllib import parse


def search(query):
    """Execute search query on the Guardian's Content Api."""

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")

        if query == "":
            orderBy = "newest"
        else:
            orderBy = "relevance"

        apiPath = f"https://content.guardianapis.com/search?order-by={orderBy}&q={query}&api-key={api_key}"
        response = requests.get(apiPath)
        response.raise_for_status()

    except requests.RequestException as e:
        print(f"Api Request Exception: {e}")
        return None

    # Parse response
    try:
        parsedResponse = response.json()
        resultsList = parsedResponse["response"]["results"]

        formattedResultsList = []
        for result in resultsList:
            formattedResult = {
                "title": result["webTitle"],
                "section": result["sectionName"],
                "date": result["webPublicationDate"],
                "url": result["webUrl"]
            }
            formattedResultsList.append(formattedResult)

        return formattedResultsList
    except (KeyError, TypeError, ValueError):
        return None

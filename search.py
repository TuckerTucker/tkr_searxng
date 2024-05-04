import requests
import logging
import json
from typing import Dict, Optional, Tuple
from tkr_simple_scrape import simple_scrape

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def search_searx(query: str, searx_url: str = "http://localhost:8080", **kwargs) -> Dict:
    """
    Make a search request to a Searx instance running in a Docker container.

    :param query: The search query string.
    :param searx_url: The URL of the Searx instance (default: "http://localhost:8080").
    :param kwargs: Additional query parameters.
    :return: The JSON response from the Searx instance.
    """
    logging.info(f"Starting search for query: {query}")

    # Prepare the query parameters
    params = {
        "q": query,
        "format": "json",
        **kwargs
    }

    try:
        # Send a GET request to the Searx instance with the search query and parameters
        response = requests.get(f"{searx_url}", params=params)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

        # Parse the JSON response
        results = response.json()

        logging.info(f"Search completed successfully. Received {len(results['results'])} results.")
        return results

    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred during the search request: {str(e)}")
        raise

def process_search_results(search_query: str, searx_url: str, save_as: Optional[str] = None,
                           return_results: bool = False, **query_params) -> Optional[list[Tuple[Dict, str]]]:
    """
    Process the search results by making a search request and scraping the result URLs.

    :param search_query: The search query string.
    :param searx_url: The URL of the Searx instance.
    :param save_as: The filename to save the search results (default: None).
    :param return_results: Whether to return the search results (default: False).
    :param query_params: Additional query parameters.
    :return: A list of tuples containing the search result and its scraped text (if return_results is True).
    """
    logging.info(f"Processing search results for query: {search_query}")

    try:
        search_results = search_searx(search_query, searx_url, **query_params)
        result_urls = (result["url"] for result in search_results["results"])
        result_texts = (simple_scrape(url) for url in result_urls)
        results = list(zip(search_results["results"], result_texts))  # Convert to list

        if save_as:
            save_json(results, save_as)
            logging.info(f"Search results saved as: {save_as}")

        if return_results:
            return results

    except Exception as e:
        logging.error(f"An error occurred while processing search results: {str(e)}")
        raise

def save_json(data: any, filename: str) -> None:
    """
    Save data as JSON.

    :param data: The data to save.
    :param filename: The filename to save the data.
    """
    logging.info(f"Saving data as JSON: {filename}")

    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=2)
        logging.info(f"Data saved successfully.")
    except IOError as e:
        logging.error(f"An error occurred while saving the data: {str(e)}")
        raise

###### Example usage
search_query = "Python programming"
searx_url = "http://localhost:8080"

# Additional query parameters
query_params = {
    "categories": "it,science",
    "language": "en",
    "pageno": 1,
    "time_range": "month",
    "safesearch": 1
}

try:
    logging.info("Starting search result processing...")
    process_search_results(search_query, searx_url, save_as="_search_results/search_results.json", return_results=True, **query_params)
    logging.info("Search result processing completed.")
except Exception as e:
    logging.error(f"An error occurred: {str(e)}")
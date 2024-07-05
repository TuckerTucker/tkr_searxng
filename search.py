# search.py
import requests
import json
import re
from typing import Dict, Optional, Tuple, List
from tkr_simple_scrape import simple_scrape
from tkr_utils.app_paths import AppPaths
from tkr_utils.config_logging import setup_logging
from tkr_utils.decorators import logs_and_exceptions

# Setup logging for this module
logger = setup_logging(__file__)

# Ensure necessary directories exist and add _search_results directory
AppPaths.check_directories()
AppPaths.add("_search_results")

@logs_and_exceptions(logger)
def search_searx(query: str, searx_url: str = "http://localhost:8080", **kwargs) -> Dict:
    """
    Make a search request to a Searx instance running in a Docker container.

    Args:
        query (str): The search query string.
        searx_url (str): The URL of the Searx instance (default: "http://localhost:8080").
        **kwargs: Additional query parameters.

    Returns:
        Dict: The JSON response from the Searx instance.
    """
    logger.info(f"Starting search for query: {query}")

    params = {
        "q": query,
        "format": "json",
        **kwargs
    }

    try:
        response = requests.get(f"{searx_url}", params=params)
        response.raise_for_status()
        results = response.json()
        logger.info(f"Search completed successfully. Received {len(results['results'])} results.")
        return results
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred during the search request: {str(e)}")
        raise

@logs_and_exceptions(logger)
def process_search_results(search_query: str, searx_url: str, save_as: Optional[str] = None,
                           return_results: bool = False, **query_params) -> Optional[List[Tuple[Dict, str]]]:
    """
    Process the search results by making a search request and scraping the result URLs.

    Args:
        search_query (str): The search query string.
        searx_url (str): The URL of the Searx instance.
        save_as (Optional[str]): The filename to save the search results (default: None).
        return_results (bool): Whether to return the search results (default: False).
        **query_params: Additional query parameters.

    Returns:
        Optional[List[Tuple[Dict, str]]]: A list of tuples containing the search result and its scraped text
                                          (if return_results is True).
    """
    logger.info(f"Processing search results for query: {search_query}")

    try:
        search_results = search_searx(search_query, searx_url, **query_params)
        result_urls = (result["url"] for result in search_results["results"])
        result_texts = (simple_scrape(url) for url in result_urls)
        results = list(zip(search_results["results"], result_texts))

        if save_as:
            save_path = AppPaths._SEARCH_RESULTS_DIR / save_as
            save_json(results, save_path)
            logger.info(f"Search results saved as: {save_path}")

        if return_results:
            return results
    except Exception as e:
        logger.error(f"An error occurred while processing search results: {str(e)}")
        raise

@logs_and_exceptions(logger)
def save_json(data: any, filename: str) -> None:
    """
    Save data as JSON.

    Args:
        data (any): The data to save.
        filename (str): The filename to save the data.
    """
    logger.info(f"Saving data as JSON: {filename}")

    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=2)
        logger.info(f"Data saved successfully.")
    except IOError as e:
        logger.error(f"An error occurred while saving the data: {str(e)}")
        raise

@logs_and_exceptions(logger)
def sanitize_filename(query: str, max_length: int = 50) -> str:
    """
    Sanitize the search query to create a valid filename and limit its length.

    Args:
        query (str): The search query string.
        max_length (int): The maximum length of the filename (default: 50).

    Returns:
        str: A sanitized and truncated filename string.
    """
    sanitized = re.sub(r'[^a-zA-Z0-9_-]', '_', query)
    return sanitized[:max_length]

if __name__ == "__main__":
    search_query = "Why did the band jellyfish breakup after only two albums in the early nineties?"
    searx_url = "http://localhost:8080"

    query_params = {
        "safesearch": 0
    }

    try:
        logger.info("Starting search result processing...")
        sanitized_query = sanitize_filename(search_query)
        save_path = f"{sanitized_query}.json"
        process_search_results(search_query, searx_url, save_as=save_path, return_results=True, **query_params)
        logger.info("Search result processing completed.")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
# Searx Search and Scrape

This project demonstrates how to perform a search using a Searx instance running in a Docker container and scrape the text content from the resulting URLs.

## Features

- Search using a Searx instance with customizable query parameters
- Basic scrape the text content from the search result URLs

## Prerequisites
- searxng-docker

```bash
git clone https://github.com/searxng/searxng-docker.git
```
> Follow the setup instructions in the searx-docker/README.md



## Installation

1. Clone the repository:

```bash
git clone https://github.com/tuckertucker/tkr_searxng

```


## Setup

1. start the venv

    ```bash
    source start_env
    ```

2. Install requirements

    ```bash
    pip install -r requirements.txt
    ```


## Usage

1. Import the necessary functions in your Python script:

    ```python
    from search import search_searx, process_search_results
    ```

2. Perform a search and process the results:
    > Note: you can simply run search.py to see this example executed

    ```python
    search_query = "Python programming"
    searx_url = "http://localhost:8080"

    query_params = {
        "categories": "it,science",
        "language": "en",
        "pageno": 1,
        "time_range": "month",
        "safesearch": 1
    }

    try:
        process_search_results(search_query, searx_url, save_as="search_results.pkl", return_results=True, **query_params)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    ```

3. The search results and scraped text will be saved in a json file specified by the `save_as` parameter.

    > Note: leaving out save_as and only using return_results will allow you to use the results in other scripts. 



## Code Overview

- `search_searx(query: str, searx_url: str = "http://localhost:8080", **kwargs) -> Dict`: Performs a search using the specified Searx instance and returns the JSON response.
- `process_search_results(search_query: str, searx_url: str, save_as: Optional[str] = None, return_results: bool = False, **query_params) -> Optional[List[Tuple[Dict, str]]]`: Processes the search results by scraping the text content from the result URLs and optionally saves the results using pickle.
- `save_object(obj: Any, filename: str) -> None`: Saves an object using pickle.
- `simple_scrape(url: str) -> Optional[str]`: Fetches the HTML content of a website and extracts the plain text from the body tag.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
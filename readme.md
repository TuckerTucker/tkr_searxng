# Searx Search and Scrape

This project demonstrates how to perform a search using a Searx instance running in a Docker container and scrape the text content from the resulting URLs.

## Features

- Search using a Searx instance with customizable query parameters
- Basic scrape the text content from the search result URLs


## Installation

1. Clone the repository:

``` bash
git clone https://github.com/tuckertucker/tkr_searxng

```

2. Setup Searx

``` bash
python _setup.py
```

## Starting Searx

Start the Searxng docker instance.
Ensure you have docker installed and running on your machine. 

``` bash
./start_searxng
```

## Searching
1. Use the python script

``` bash
python search.py
```

This will search and save the results as a json in _search_results

import requests
import logging
import re
from typing import Optional
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def simple_scrape(url: str) -> Optional[str]:
    """
    Fetches the HTML content of a website and extracts the plain text from the body tag.

    :param url: The URL of the website to scrape.
    :return: The extracted plain text from the body tag, or None if an error occurs.
    """
    logging.info(f"Fetching text from URL: {url}")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
    }

    try:
        with requests.get(url, headers=headers) as response:
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            body = soup.body
            if body is None:
                raise ValueError("No body tag found in the HTML.")

            logging.info("Removing script and style tags")
            for tag in body(["script", "style"]):
                tag.decompose()

            logging.info("Extracting and cleaning text content")
            text = re.sub(r'[\n\t]{2,}', '\n\n', body.get_text(separator='\n')).strip()

            if not text:
                logging.warning("Extracted text is empty.")
                return None

            logging.info("Text extraction completed successfully")
            return text

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching the website: {e}")
        return None

    except (ValueError, AttributeError) as e:
        logging.error(f"Error parsing the HTML: {e}")
        return None

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return None
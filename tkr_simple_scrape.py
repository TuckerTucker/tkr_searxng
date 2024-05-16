import argparse
import requests
import logging
import html2text
from typing import Optional
from bs4 import BeautifulSoup
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def html_to_markdown(html: str) -> str:
    """
    Converts HTML content to Markdown format.
    """
    converter = html2text.HTML2Text()
    converter.ignore_links = False
    markdown = converter.handle(html)
    return markdown

def create_filename_from_url(url: str, is_html: bool = True, img_only: bool = False) -> str:
    """
    Creates a valid filename from a URL by removing the protocol, 'www.', replacing non-filename characters with hyphens, and appending an appropriate file extension.
    """
    filename = re.sub(r'^https?://(www\.)?', '', url)
    filename = re.sub(r'[^a-zA-Z0-9]', '-', filename).strip('-')
    if img_only:
        filename += '.img-only'
    extension = '.html' if is_html else '.md'
    return filename + extension

def simple_scrape(url: str, export_html: bool = False, img_only: bool = False) -> Optional[str]:
    """
    Fetches the HTML content of a website and processes it according to the chosen export mode.
    """
    logging.info(f"Fetching content from URL: {url}")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        for tag in soup(['script', 'style', 'template', 'svg']):
            tag.decompose()

        if img_only:
            images = soup.find_all('img')
            list_html = "<ul>" + "".join(f"<li><img src='{img['src']}' alt='{img.get('alt', '')}'></li>" for img in images if img.has_attr('src')) + "</ul>"
            return list_html

        if export_html:
            return str(soup)
    
        body_content = soup.find('body')
        if body_content is None:
            logging.warning("No <body> tag found in the HTML content.")
            return None
        
        html_content = str(body_content)
        markdown_content = html_to_markdown(html_content)
        if not markdown_content.strip():
            logging.warning("Conversion to Markdown resulted in empty content.")
            return None
        
        return markdown_content

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching the website: {e}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Scrape a website and export it as either Markdown, cleaned HTML or HTML list of images.")
    parser.add_argument('--url', type=str, required=True, help='The URL of the website to scrape.')
    parser.add_argument('--html', action='store_true', help='Export as HTML, default is Markdown')
    parser.add_argument('--img-only', action='store_true', help='Export only images as HTML list')

    args = parser.parse_args()

    if args.img_only:
        result = simple_scrape(args.url, img_only=True)
        filename = create_filename_from_url(args.url, is_html=True, img_only=True)
    elif args.html:
        result = simple_scrape(args.url, export_html=True)
        filename = create_filename_from_url(args.url, is_html=True)
    else:
        result = simple_scrape(args.url)
        filename = create_filename_from_url(args.url)

    if result:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(result)
        logging.info(f"Content written to {filename}")
    else:
        logging.error("Failed to process the content properly.")

if __name__ == "__main__":
    main()
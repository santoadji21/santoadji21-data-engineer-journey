"""
Web Scraper — extract quotes from https://quotes.toscrape.com

This site is specifically designed for scraping practice (safe to scrape).

Libraries used:
  - requests   : HTTP client — sends GET/POST requests to web servers
  - BeautifulSoup (bs4) : HTML parser — navigates and extracts data from HTML

Usage:
    python -m ETL.scraper.quotes_spider
    python -m ETL.scraper.quotes_spider --pages 5 --output data/quotes.json
"""

import json
import time
import logging
from pathlib import Path

import requests
# requests.get(url) sends an HTTP GET request and returns a Response object
# Response.status_code : HTTP status (200=OK, 404=Not Found, etc.)
# Response.text        : response body as a string (the HTML)
# Response.json()      : parse response body as JSON

from bs4 import BeautifulSoup
# BeautifulSoup(html, parser) creates a parse tree from HTML
# .find()     : find the FIRST matching element
# .find_all() : find ALL matching elements
# .select()   : find elements using CSS selectors (like jQuery)
# .text       : get the text content of an element (strips HTML tags)
# .get(attr)  : get an HTML attribute value (e.g., href, class)

# ============================================================
# Setup logging
# ============================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("quotes_spider")


# ============================================================
# Scraper Functions
# ============================================================

BASE_URL = "https://quotes.toscrape.com"


def scrape_page(url: str) -> tuple[list[dict], str | None]:
    """
    Scrape a single page of quotes.

    Args:
        url: Full URL of the page to scrape

    Returns:
        Tuple of (list_of_quotes, next_page_url_or_None)
    """
    logger.info(f"Fetching: {url}")

    # --- Send HTTP request ---
    response = requests.get(url, timeout=10)
    # timeout=10 : abort if the server doesn't respond within 10 seconds

    # raise_for_status() raises an HTTPError if status is 4xx or 5xx
    response.raise_for_status()

    # --- Parse HTML ---
    # 'html.parser' is Python's built-in HTML parser (no extra install needed)
    # Other options: 'lxml' (faster), 'html5lib' (most lenient)
    soup = BeautifulSoup(response.text, "html.parser")

    # --- Extract quotes ---
    quotes = []

    # find_all('div', class_='quote') finds all <div class="quote"> elements
    for quote_div in soup.find_all("div", class_="quote"):
        # .find('span', class_='text') finds the first <span class="text"> inside
        text = quote_div.find("span", class_="text").text
        # .text extracts the inner text content, stripping HTML tags

        author = quote_div.find("small", class_="author").text

        # .find_all('a', class_='tag') finds all tag links
        tags = [tag.text for tag in quote_div.find_all("a", class_="tag")]

        # Get author detail URL
        author_link = quote_div.find("a")
        # .get('href') extracts the href attribute value
        author_url = BASE_URL + author_link.get("href") if author_link else None

        quotes.append({
            "text": text,
            "author": author,
            "tags": tags,
            "author_url": author_url,
        })

    # --- Find next page ---
    # The "Next" button is inside <li class="next"><a href="/page/2/">
    next_btn = soup.find("li", class_="next")
    next_url = None
    if next_btn:
        next_link = next_btn.find("a")
        if next_link:
            next_url = BASE_URL + next_link.get("href")

    return quotes, next_url


def scrape_all_quotes(max_pages: int = 10, delay: float = 1.0) -> list[dict]:
    """
    Scrape multiple pages of quotes, following pagination.

    Args:
        max_pages : maximum number of pages to scrape
        delay     : seconds to wait between requests (be polite to the server!)

    Returns:
        List of all scraped quote dicts
    """
    all_quotes = []
    url = BASE_URL
    page = 1

    while url and page <= max_pages:
        quotes, next_url = scrape_page(url)
        all_quotes.extend(quotes)
        # list.extend() adds all items from another list (like += but clearer)

        logger.info(f"  Page {page}: scraped {len(quotes)} quotes (total: {len(all_quotes)})")

        url = next_url
        page += 1

        if url:
            # Be a good citizen: wait between requests to avoid overloading the server
            time.sleep(delay)

    return all_quotes


def save_quotes(quotes: list[dict], output_path: str | Path) -> Path:
    """
    Save scraped quotes to a JSON file.

    Args:
        quotes     : list of quote dicts
        output_path: file path to save to

    Returns:
        Path object of the saved file
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    # json.dump() writes Python object directly to a file handle
    # (vs json.dumps() which returns a string)
    with path.open("w", encoding="utf-8") as f:
        json.dump(quotes, f, indent=2, ensure_ascii=False)

    logger.info(f"Saved {len(quotes)} quotes → {path}")
    return path


# ============================================================
# CLI Entry Point
# ============================================================

def main():
    """Run the scraper from the command line."""
    import argparse

    # argparse creates a command-line argument parser
    parser = argparse.ArgumentParser(description="Scrape quotes from quotes.toscrape.com")
    parser.add_argument("--pages", type=int, default=10, help="Max pages to scrape")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between requests (seconds)")
    parser.add_argument(
        "--output",
        type=str,
        default="ETL/scraper/output/quotes_raw.json",
        help="Output file path",
    )
    args = parser.parse_args()

    logger.info(f"Starting scraper: max_pages={args.pages}, delay={args.delay}s")

    quotes = scrape_all_quotes(max_pages=args.pages, delay=args.delay)
    save_quotes(quotes, args.output)

    logger.info(f"Done! Scraped {len(quotes)} quotes total.")
    return quotes


if __name__ == "__main__":
    main()

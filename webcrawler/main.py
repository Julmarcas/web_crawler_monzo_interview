import time
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from urllib.parse import urljoin
from urllib.parse import urlparse

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class LinkParser(HTMLParser):
    """
    A class for parsing HTML and extracting links.

    Attributes:
        base_url (str): The base URL of the HTML page being parsed.
        links (list): A list of extracted links.

    Methods:
        handle_starttag(tag, attrs): Handles the start tag of an HTML element.
    """

    def __init__(self, base_url: str) -> None:
        super().__init__()
        self.base_url = base_url
        self.links: list[str] = []

    def handle_starttag(self, tag, attrs) -> None:
        """
        Handles the start tag of an HTML element.

        Args:
            tag (str): The name of the HTML tag.
            attrs (list): A list of (name, value) pairs representing the attributes of the tag.

        Returns:
            None
        """
        if tag == "a":
            for attr, value in attrs:
                if attr == "href":
                    self.links.append(value)


class WebCrawler:
    def __init__(self, url: str, max_workers: int = 5):
        self.start_url = url
        self.base_url = urlparse(url).scheme + "://" + urlparse(url).netloc
        self.visited_urls: set[str] = set()
        self.new_links: set[str] = set()
        self.link_counter = 0
        self.max_workers = max_workers

        # Retry 3 times with a backoff factor of 0.5 seconds
        retries = Retry(
            total=3, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504]
        )
        self.session = requests.Session()
        self.session.mount("http://", HTTPAdapter(max_retries=retries))
        self.session.mount("https://", HTTPAdapter(max_retries=retries))

    def is_same_subdomain(self, url: str) -> bool:
        """
        Check if the given URL belongs to the same subdomain as the start URL.

        Args:
            url (str): The URL to check.

        Returns:
            bool: True if the URL belongs to the same subdomain, False otherwise.
        """
        return urlparse(url).netloc == urlparse(self.start_url).netloc

    def parse_links(self, html_content: str) -> set:
        """
        Parses the HTML content and extracts the links that belong to the same subdomain as the start URL.

        Args:
            html_content (str): The HTML content to parse.

        Returns:
            set: A set of links that belong to the same subdomain as the start URL.
        """
        parser = LinkParser(self.base_url)
        try:
            parser.feed(html_content)
        except AssertionError as e:
            print(f"Error parsing HTML content: {e}")
            return set()
        parser.feed(html_content)
        return {
            urljoin(self.start_url, link)
            for link in parser.links
            if link and self.is_same_subdomain(urljoin(self.start_url, link))
        }

    def crawl(self, current_url: str) -> None:
        """
        Crawls the given URL and its subdomains, recursively following links.

        Args:
            current_url (str): The URL to crawl.

        Returns:
            None
        """
        if current_url in self.visited_urls or not self.is_same_subdomain(current_url):
            return

        print("Checking:", current_url)
        self.visited_urls.add(current_url)

        try:
            response = self.session.get(current_url, timeout=5)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
            links = self.parse_links(response.text)
            new_links = links - self.visited_urls - self.new_links
            self.new_links.update(new_links)
            self.link_counter += len(new_links)
            self.print_links(links)

            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = [executor.submit(self.crawl, link) for link in new_links]

                for future in futures:
                    future.result()

        except requests.RequestException as e:
            print(f"Error crawling {current_url}: {e}")

    def print_links(self, links):
        """
        Print the list of links found on a page.

        Args:
            links (list): A list of links to be printed.
        """
        print("list of links found on this page:")
        for link in links:
            print("-", link)

    def start(self) -> None:
        """
        Starts the web crawling process from the start URL.
        """
        self.crawl(self.start_url)
        print("Total number of unique new links found:", self.link_counter)


if __name__ == "__main__":
    START_URL = "https://monzo.com"
    crawler = WebCrawler(START_URL, max_workers=3)
    start_time = time.time()
    try:
        crawler.start()
    finally:
        elapsed_time = time.time() - start_time
        print("Elapsed time: ", elapsed_time)

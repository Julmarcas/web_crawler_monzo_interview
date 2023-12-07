from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
import requests

from webcrawler.main import LinkParser
from webcrawler.main import WebCrawler


class TestWebCrawler:
    """
    Test class for the WebCrawler class.
    """

    @pytest.fixture
    def web_crawler_instance(self):
        """
        Creates an instance of the WebCrawler class.

        Returns:
            WebCrawler: An instance of the WebCrawler class.
        """
        test_url = "https://example.com"
        return WebCrawler(test_url)

    @patch.object(requests.Session, "get")
    def test_crawl(self, mock_get, web_crawler_instance):
        """
        Test the crawl method of the WebCrawler class.
        """

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
                <html>
                    <body>
                        <a href="https://www.example.com/about">About</a>
                        <a href="https://www.example.com/info">Info</a>
                    </body>
                </html>
                """

        mock_get.return_value = mock_response

        web_crawler_instance.parse_links = MagicMock(return_value={"/about", "/info"})

        web_crawler_instance.crawl("https://example.com")

        web_crawler_instance.parse_links.assert_called_with(
            """
                <html>
                    <body>
                        <a href="https://www.example.com/about">About</a>
                        <a href="https://www.example.com/info">Info</a>
                    </body>
                </html>
                """
        )

    @patch.object(requests.Session, "get")
    def test_crawl_recursion(self, mock_get, web_crawler_instance):
        """
        Test case for the crawl method with recursion.

        This test case verifies that the crawl method is called recursively for each page
        encountered during the crawling process.
        """

        response1 = MagicMock()
        response1.status_code = 200
        response1.text = "<html><body><a href='/page1'></a></body></html>"

        response2 = MagicMock()
        response2.status_code = 200
        response2.text = "<html><body><a href='/page2'></a></body></html>"

        response3 = MagicMock()
        response3.status_code = 200
        response3.text = ""
        mock_get.side_effect = [response1, response2, response3]

        web_crawler_instance.crawl = MagicMock(wraps=web_crawler_instance.crawl)

        web_crawler_instance.crawl("https://example.com")

        assert web_crawler_instance.crawl.call_count == 3

    def test_is_same_subdomain(self):
        """
        Test case for the is_same_subdomain method of the WebCrawler class.
        """
        crawler = WebCrawler("https://www.example.com")
        assert crawler.is_same_subdomain("https://www.example.com/about")
        assert not crawler.is_same_subdomain("https://www.example.org")
        assert not crawler.is_same_subdomain("https://www.sub.example.org")

    def test_parse_links(self):
        """
        Test case for the parse_links method of the WebCrawler class.
        """
        crawler = WebCrawler("https://www.example.com")
        links = crawler.parse_links(
            """
            <html>
                <body>
                    <a href="/about">About</a>
                    <a href="https://www.example.com/about">About</a>
                    <a href="https://www.example.org/about">About</a>
                    <a href="https://www.sub.example.org/about">About</a>
                    <a href="https://www.example.com/info">Info</a>
                </body>
            </html>
            """
        )
        assert links == {
            "https://www.example.com/about",
            "https://www.example.com/info",
        }


class TestLinkParser:
    """
    Test class for the LinkParser class.
    """

    def test_handle_starttag(self):
        """
        Test case for the handle_starttag method of the LinkParser class.
        """
        link_parser = LinkParser("https://www.google.com")
        link_parser.handle_starttag("a", [("href", "https://www.google.com/about")])

        assert len(link_parser.links) == 1
        assert "https://www.google.com/about" in link_parser.links

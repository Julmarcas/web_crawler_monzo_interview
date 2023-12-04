from webcrawler.main import WebCrawler, LinkParser


def test_handle_starttag():
    link_parser = LinkParser("https://www.google.com")
    link_parser.handle_starttag("a", [("href", "https://www.google.com/about")])


def test_is_same_subdomain():
    crawler = WebCrawler("https://www.example.com")
    assert crawler.is_same_subdomain("https://www.example.com/about")
    assert not crawler.is_same_subdomain("https://www.example.org")
    assert not crawler.is_same_subdomain("https://www.sub.example.org")


def test_parse_links():
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
    assert links == {"https://www.example.com/about", "https://www.example.com/info"}

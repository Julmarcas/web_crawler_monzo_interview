# WebCrawler

A simple web crawler written in Python that recursively crawls a website, prints the links found on each page, and counts the total number of unique new links.

## Requirements

- Python 3.12
- [Poetry](https://python-poetry.org/docs/) 1.7.1 - tool for dependency management and packaging

## Getting Started

1. Meet the [requirements](#requirements)
2. Install the dependencies using Poetry: `poetry install`
3. Follow [Usage](#usage) to execute the project.

## Usage

To start the web crawler, run the following command:

- `poetry run python3 -m webcrawler.main`
- `make run`

## Tests

To execute the tests and generate the coverage report run one of the following commands:

- `poetry run pytest -vv --cov=webcrawler --cov-report=term-missing --cov-report=html`
- `make test`

See the pytest docs for more cli options: [pytest-usage](https://docs.pytest.org/en/6.2.x/usage.html)

## Pre-commit

This project incorporates pre-commit integration, featuring a set of hooks meticulously designed to uphold and maintain coding standards.

To execute pre-commit:

- Install [pre-commit](https://pre-commit.com/) 3.5.0
- Set up pre-commit hooks: `pre-commit install`
- Execute all pre-commit hooks without committing changes: `run --all-files`

## Decision Log

- **HTML Parsing Technique:**

  - Decision: Utilize HTMLParser instead of BeautifulSoup for HTML parsing.
  - Rationale: Simplifies usage, avoids adding dependencies, and aligns with the project's focus on extracting links.
  - Consideration: The basic parser may struggle with complex HTML structures or malformed HTML.

- **Request Timeout Setting:**

  - Decision: Set a fixed timeout of 5 seconds for each request.
  - Rationale: Ensures a uniform timeout across requests for simplicity.
  - Consideration: Different pages might necessitate varied timeout values; dynamic adjustment based on response time could be explored for flexibility.

- **Logging Approach:**

  - Decision: Adopt minimal logging, with outputs to the console for simplicity.
  - Rationale: Time constraints.
  - Consideration: For a production-level application, comprehensive logging with log levels could enhance debugging and monitoring.

- **Handling HTTP Error 443:**

  - Challenge: Faced an expected HTTP error 443.
  - Solution: Implemented a retry mechanism with delays between requests.

- **Execution Time Calculation:**

  - Logic: Integrated functionality to calculate execution time.
  - Purpose: Facilitates analysis of results under different configuration parameters.

- **Unique Links Tracking:**
  - Logic: Implemented a mechanism to count the number of unique links visited.
  - Purpose: Driven by curiosity, adds a metric for evaluating the scale of link exploration.

## Improvements

Areas where I believe this exercise could be enhanced exist, yet I refrained from implementing them to adhere to the suggested time constraints.

- **Logging Over Printing:** Develop a robust logging system tailored for a production environment, incorporating various levels, and capable of documenting visited links.

- **Exception Handling Enhancement:** Elevate the exception-handling mechanism by capturing more specific exceptions, enabling the appropriate handling of diverse error types.

- **Test Coverage Augmentation:** Enhance the current test coverage, currently standing at 81%, to ensure a more comprehensive examination of the codebase.

- **CLI Tool Encapsulation:** Encapsulate the tool as a command-line interface (CLI) tool using a library such as [Typer](https://typer.tiangolo.com/). This allows efficient command line argument management and configuration, enhancing usability and accessibility.

## Tests performed and results

I have conducted numerous tests employing various configurations for the workers, and the ensuing results are as follows:

- Workers 3:
  - Total number of unique new links found: 3505
  - Elapsed time: 102.97893023490906
- Workers 2:
  - Total number of unique new links found: 3506
  - Elapsed time: 90.97998714447021
- Workers 1:
  - Total number of unique new links found: 3507
  - Elapsed time: 557.209639787674

This represents only a subset of the comprehensive tests conducted. While the count of unique links exhibits relative stability, the elapsed time naturally fluctuates based on response times. Notably, there is a discernible enhancement in overall performance.

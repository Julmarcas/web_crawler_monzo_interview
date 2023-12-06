# WebCrawler

A simple web crawler written in Python that recursively crawls a website, prints the links found on each page, and counts the total number of unique new links.

## Requirements

- Python ^3.12
- Poetry 1.7.1 - tool for dependency management and packaging

## Getting Started

1. Meet the [requirements](#requirements)
2. Install the dependencies using Poetry: `poetry install`

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

This project includes the configuration for pre-commit integration, with a set of hooks intended to preserve standards.

To execute pre-commit:

- Set up pre-commit hooks: `pre-commit install`
- Execute all pre-commit hooks without committing changes: `run --all-files`

## Decision log

- Use HTMLParser instead of BeautifulSoup for html parsing as it simplifies its use, does not add dependencies and the only element we are currently interested in for this project are the links.
  - Consideration: This basic parser may not handle complex HTML structures or malformed HTML.
- A fixed timeout of 5 seconds is used for each request.
  - Consideration: Different pages may require different timeout values. Dynamic adjustment based on response time or handling timeouts more gracefully could be considered.
- Logging is minimal, printing to the console for simplicity
  - Consideration: For a production-level application, more comprehensive logging, possibly with log levels, could aid in debugging and monitoring.
- I faced expected HTTP error 443, implemented a retry mechanism with delays between requests.
- Logic has been integrated to calculate the execution time in order to be able to analyse results based on different configuration parameters.
- Logic has been implemented to calculate the number of unique links visited, just out of curiosity.

## Improvements

Points on which I consider that this exercise can be improved but which I have not applied in order to keep within the suggested time scale.

- Logging instead of Printing: Generate a log system suitable for a production system, with different levels and that can be used to print the visited links.
- Exception Handling; Improve the handling of exceptions by capturing more specific exceptions that allow handling different types of errors appropriately.
- Test coverage: Increase test coverage, currently 80%.
- Encapsulate the tool as a cli tool using a library such as [Typer](https://typer.tiangolo.com/) that allows command line argument management and configuration.

## Tests performed and results

I have done several tests with different configurations for the workers and these are the results:

- Workers 3:
  - Total number of unique new links found: 3505
  - Elapsed time: 102.97893023490906
- Workers 2:
  - Total number of unique new links found: 3506
  - Elapsed time: 90.97998714447021
- Workers 1:
  - Total number of unique new links found: 3507
  - Elapsed time: 557.209639787674

This is just a sample of all the tests carried out. The number of unique links remains relatively stable but the time can obviously vary depending on the response time, but there is a clear improvement in performance.

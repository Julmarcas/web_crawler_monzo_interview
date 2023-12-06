# Purpose: Makefile for webcrawler

default: help

help:           ## Show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

run: 		  ## Run the webcrawler
	poetry run python3 -m webcrawler.main

test: 		  ## Run the tests
	poetry run pytest -vv --cov=webcrawler --cov-report=term-missing --cov-report=html

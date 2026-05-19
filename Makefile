.PHONY: setup test lint format demo hooks

setup:
	python -m pip install -r requirements.txt -r requirements-dev.txt

test:
	pytest

lint:
	ruff check .

format:
	ruff format .

hooks:
	./scripts/install-hooks.sh

demo:
	python -m app.report

.PHONY: format lint test check run benchmark api clean install dev

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

format:
	black src tests scripts

lint:
	ruff check src tests scripts --fix
	mypy src

test:
	pytest -q

check: format lint test

run:
	python -m pygobang.app.main

api:
	python scripts/run_api.py

benchmark:
	python scripts/run_benchmark.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache build dist *.egg-info

SRC = ./src/mazegen/generator.py \
	./src/mazegen/__init__.py \
	./tests/test_basics.py

MYPY_OPTIONS := --warn-return-any \
	--warn-unused-ignores \
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--check-untyped-defs

SYNC := .synced

build:
	uv build

install: $(SYNC)

$(SYNC): pyproject.toml
	git config core.hooksPath .githooks
	uv sync || pip install uv && uv sync
	@touch $(SYNC)
	
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf dist/
	rm -rf $(SYNC)

lint-strict: $(SYNC)
	ruff check $(SRC)
	uv run flake8 $(SRC)
	uv run mypy $(SRC) --strict

format:
	ruff format $(SRC)

test: $(SYNC)
	uv run pytest

re: clean build

	
.PHONY: build install clean lint-strict format test re

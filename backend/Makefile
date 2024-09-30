WORKDIR = $(shell pwd)
.PHONY: runtime-envs process help

DB_URL ?= postgresql://investors:password@localhost/investors

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)


format:  ## reformat code using linter
	poetry run ruff format .
	poetry run ruff check . --fix

validate: check typecheck test ## run linter and typechecker

check:  ## check code using linter
	poetry run ruff check .

typecheck:  ## check the types with mypy
	poetry run mypy . --enable-incomplete-feature=NewGenericSyntax

test: ## run all tests
	poetry run python -m pytest tests

install-dev-deps:  ## install development dependencies
	poetry install --with=dev


start: ## start FastApi server
	DB_URL=$(DB_URL) poetry run python -m uvicorn backend.app:app --host=0.0.0.0 --port 8080 --workers=1

start-dev: ## start FastApi server
	DB_URL=$(DB_URL) poetry run python -m uvicorn backend.app:app --host=0.0.0.0 --port 8080 --reload


define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
        match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
        if match:
                target, help = match.groups()
                print("%-30s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

